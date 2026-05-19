from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import FileResponse
from .google_sheets import find_row_by_cedula, buscar_departamento_por_ciudad, get_sheet_data, SPREADSHEET_ID_2
from .pdf_generator import (
    rellenar_pdf_empleado,
    generar_nombre_archivo_pdf,
    CONFIGURACION_FORMATOS,
)
import os
import tempfile
import uuid
import zipfile
from urllib.parse import urlencode
from pathlib import Path
from django.conf import settings


def _normalizar_resultado_busqueda(result_data):
    return {
        'CEDULA': result_data.get('CEDULA', ''),
        'PRIMER_APELLIDO': result_data.get('PRIMER APELLIDO', ''),
        'SEGUNDO_APELLIDO': result_data.get('SEGUNDO APELLIDO', ''),
        'NOMBRES': result_data.get('NOMBRES', ''),
        'FECHA_NACIMIENTO': result_data.get('FECHA DE NACIMIENTO', ''),
        'PAIS_NACIMIENTO': result_data.get('PAIS DE NACIMIENTO', ''),
        'CODIGO_SEXO': result_data.get('CODIGO SEXO', ''),
        'DEPARTAMENTO_NACIMIENTO': result_data.get('DEPARTAMENTO NACIMIENTO', ''),
        'CIUDAD_NACIMIENTO': result_data.get('CIUDAD DE NACIMIENTO', ''),
        'EPS': result_data.get('EPS', ''),
        'EMPRESA': result_data.get('EMPRESA', ''),
        'AREA': result_data.get('AREA', ''),
        'PROGRAMA AL QUE PERTENECE': result_data.get('PROGRAMA AL QUE PERTENECE', ''),
        '_origen_hoja': result_data.get('_origen_hoja', ''),
    }


def _normalizar_datos_para_pdf(datos_empleado):
    return {
        'CEDULA': datos_empleado.get('CEDULA', ''),
        'PRIMER_APELLIDO': datos_empleado.get('PRIMER APELLIDO', ''),
        'SEGUNDO_APELLIDO': datos_empleado.get('SEGUNDO APELLIDO', ''),
        'NOMBRES': datos_empleado.get('NOMBRES', ''),
        'FECHA_NACIMIENTO': datos_empleado.get('FECHA DE NACIMIENTO', ''),
        'PAIS_NACIMIENTO': datos_empleado.get('PAIS DE NACIMIENTO', ''),
        'CODIGO_SEXO': datos_empleado.get('CODIGO SEXO', ''),
        'DEPARTAMENTO_NACIMIENTO': datos_empleado.get('DEPARTAMENTO NACIMIENTO', ''),
        'CIUDAD_NACIMIENTO': datos_empleado.get('CIUDAD DE NACIMIENTO', ''),
        'EPS': datos_empleado.get('EPS', ''),
        'AFP': datos_empleado.get('AFP', ''),
        'SALARIO_BASICO': datos_empleado.get('SALARIO BASICO', ''),
        'CORREO_ELECTRONICO': datos_empleado.get('CORREOS', ''),
        'DIRECCION_RESIDENCIA': datos_empleado.get('DIRECCION DE VIVIENDA', ''),
        'TELEFONO_MOVIL': datos_empleado.get('NUMERO TELEFONICO ', '').strip(),
        'BARRIO': datos_empleado.get('BARRIO', ''),
        'CIUDAD_RESIDENCIA': datos_empleado.get('CIUDAD') or datos_empleado.get('MUNICIPIO', ''),
        'DEPARTAMENTO_POR_CIUDAD': buscar_departamento_por_ciudad(
            datos_empleado.get('CIUDAD') or datos_empleado.get('MUNICIPIO', '')
        ),
        'EMPRESA': datos_empleado.get('EMPRESA', ''),
        'AREA': datos_empleado.get('AREA', ''),
        'PROGRAMA AL QUE PERTENECE': datos_empleado.get('PROGRAMA AL QUE PERTENECE', ''),
        '_origen_hoja': datos_empleado.get('_origen_hoja', ''),
        'FECHA_INGRESO': datos_empleado.get('FECHA DE INGRESO (AAAAMMDD)', ''),
    }


def _parsear_cedulas(raw_value):
    if not raw_value:
        return []

    tokens = []
    actual = []
    for ch in str(raw_value):
        if ch.isdigit():
            actual.append(ch)
        else:
            if actual:
                tokens.append(''.join(actual))
                actual = []
    if actual:
        tokens.append(''.join(actual))

    cedulas_limpias = []
    vistas = set()
    for cedula in tokens:
        if cedula and cedula not in vistas:
            vistas.add(cedula)
            cedulas_limpias.append(cedula)
    return cedulas_limpias


def _to_upper(value):
    return str(value or '').strip().upper()


def _to_int_fecha(fecha_str):
    fecha_limpia = str(fecha_str or '').strip()
    if len(fecha_limpia) != 8 or not fecha_limpia.isdigit():
        return 0
    return int(fecha_limpia)


def _es_activo(row):
    """
    Regla flexible de activo:
    - Si FECHA RETIRO tiene valor -> inactivo
    - Si ESTADO existe -> activo solo si es ACTIVO
    - Si ACTIVO existe -> activo para SI/TRUE/1/ACTIVO/VIGENTE
    - Si no hay columnas de estado/retiro -> se considera activo
    """
    fecha_retiro = str(row.get('FECHA RETIRO', '')).strip()
    if fecha_retiro:
        return False

    estado = _to_upper(row.get('ESTADO', ''))
    if estado:
        return estado == 'ACTIVO'

    activo = _to_upper(row.get('ACTIVO', ''))
    if activo:
        return activo in {'SI', 'SÍ', 'TRUE', '1', 'ACTIVO', 'VIGENTE'}

    return True


def _obtener_registros_unificados():
    planta_data = get_sheet_data('Planta')
    planta_data_2 = get_sheet_data('Planta', SPREADSHEET_ID_2)
    manipuladoras_data = get_sheet_data('Manipuladoras')

    rows = []
    for row in planta_data:
        row['_origen_hoja'] = 'Planta'
        rows.append(row)
    for row in planta_data_2:
        row['_origen_hoja'] = 'Planta'
        rows.append(row)
    for row in manipuladoras_data:
        row['_origen_hoja'] = 'Manipuladoras'
        rows.append(row)

    # Si hay cédulas repetidas, conservar el más reciente por FECHA DE INGRESO
    por_cedula = {}
    for row in rows:
        cedula = str(row.get('CEDULA', '')).strip()
        if not cedula:
            continue

        if cedula not in por_cedula:
            por_cedula[cedula] = row
            continue

        actual_fecha = _to_int_fecha(row.get('FECHA DE INGRESO (AAAAMMDD)', ''))
        previo_fecha = _to_int_fecha(por_cedula[cedula].get('FECHA DE INGRESO (AAAAMMDD)', ''))
        if actual_fecha >= previo_fecha:
            por_cedula[cedula] = row

    return list(por_cedula.values())


def _filtrar_registros(rows, filtros):
    eps = _to_upper(filtros.get('eps'))
    origen = _to_upper(filtros.get('origen_hoja'))
    empresa = _to_upper(filtros.get('empresa'))
    area = _to_upper(filtros.get('area'))
    programa = _to_upper(filtros.get('programa'))
    ciudad = _to_upper(filtros.get('ciudad'))
    fecha_desde = _to_int_fecha(filtros.get('fecha_ingreso_desde'))
    fecha_hasta = _to_int_fecha(filtros.get('fecha_ingreso_hasta'))
    solo_activos = filtros.get('solo_activos') == 'on'
    solo_eps_configurada = filtros.get('solo_eps_configurada') == 'on'

    resultado = []
    for row in rows:
        row_eps = _to_upper(row.get('EPS'))
        row_origen = _to_upper(row.get('_origen_hoja'))
        row_empresa = _to_upper(row.get('EMPRESA'))
        row_area = _to_upper(row.get('AREA'))
        row_programa = _to_upper(row.get('PROGRAMA AL QUE PERTENECE'))
        row_ciudad = _to_upper(row.get('CIUDAD') or row.get('MUNICIPIO'))
        row_fecha = _to_int_fecha(row.get('FECHA DE INGRESO (AAAAMMDD)', ''))

        if eps and row_eps != eps:
            continue
        if origen and row_origen != origen:
            continue
        if empresa and empresa not in row_empresa:
            continue
        if area and area not in row_area:
            continue
        if programa and programa not in row_programa:
            continue
        if ciudad and ciudad not in row_ciudad:
            continue
        if fecha_desde and (not row_fecha or row_fecha < fecha_desde):
            continue
        if fecha_hasta and (not row_fecha or row_fecha > fecha_hasta):
            continue
        if solo_activos and not _es_activo(row):
            continue
        if solo_eps_configurada and not CONFIGURACION_FORMATOS.get(row_eps):
            continue

        resultado.append(row)

    return resultado


def login_view(request):
    if request.user.is_authenticated:
        return redirect('formatos_eps:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('formatos_eps:dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'formatos_eps/login.html')


@login_required(login_url='formatos_eps:login')
def dashboard_view(request):
    return render(request, 'formatos_eps/dashboard.html')


@login_required(login_url='formatos_eps:login')
@permission_required('formatos_eps.ver_eps', login_url='formatos_eps:dashboard', raise_exception=False)
def search_view(request):
    formatos_dir = Path(settings.BASE_DIR).parent / 'formatos'
    eps_disponibles = []
    for eps, config in CONFIGURACION_FORMATOS.items():
        if not eps or not isinstance(config, dict):
            continue
        archivo = config.get('archivo')
        if not archivo:
            continue
        if (formatos_dir / archivo).exists():
            eps_disponibles.append(eps)

    eps_disponibles = sorted(eps_disponibles)
    return render(request, 'formatos_eps/search.html', {'eps_disponibles': eps_disponibles})


@login_required(login_url='formatos_eps:login')
@permission_required('formatos_eps.ver_eps', login_url='formatos_eps:dashboard', raise_exception=False)
def search_results_view(request):
    cedula = request.GET.get('cedula')
    results = None
    error_message = None

    if cedula:
        try:
            result_data = find_row_by_cedula(cedula)
            if result_data:
                results = _normalizar_resultado_busqueda(result_data)
        except ConnectionError:
            error_message = 'Error de conexión con Google Sheets. Por favor, verifique la configuración de credenciales.'
            messages.error(request, error_message)
        except Exception as e:
            error_message = f'Error al buscar la cédula: {str(e)}'
            messages.error(request, error_message)

    return render(request, 'formatos_eps/search_results.html', {
        'results': [results] if results else [],
        'cedula': cedula,
        'error_message': error_message
    })


@login_required(login_url='formatos_eps:login')
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('formatos_eps:login')


@login_required(login_url='formatos_eps:login')
@permission_required('formatos_eps.ver_eps', login_url='formatos_eps:dashboard', raise_exception=False)
def generar_pdf_view(request, cedula):
    """
    Vista para generar y descargar el PDF del formulario EPS con los datos del empleado.
    """
    try:
        datos_empleado = find_row_by_cedula(cedula)

        if not datos_empleado:
            messages.error(request, f'No se encontró empleado con cédula {cedula}')
            query_string = urlencode({'cedula': cedula})
            return redirect(f"{redirect('formatos_eps:search_results').url}?{query_string}")

        datos_normalizados = _normalizar_datos_para_pdf(datos_empleado)

        nombre_archivo = generar_nombre_archivo_pdf(cedula, datos_normalizados.get('PRIMER_APELLIDO', ''))
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, nombre_archivo)

        rellenar_pdf_empleado(datos_normalizados, output_path)

        return FileResponse(
            open(output_path, 'rb'),
            content_type='application/pdf',
            as_attachment=True,
            filename=nombre_archivo
        )

    except ValueError as e:
        messages.error(request, str(e))
        return redirect('formatos_eps:search_results')
    except ConnectionError:
        messages.error(request, 'Error de conexión con Google Sheets')
        return redirect('formatos_eps:search')
    except FileNotFoundError:
        messages.error(request, 'No se encontró el archivo PDF template')
        return redirect('formatos_eps:search')
    except Exception as e:
        messages.error(request, f'Error al generar el PDF: {str(e)}')
        return redirect('formatos_eps:search')


@login_required(login_url='formatos_eps:login')
@permission_required('formatos_eps.ver_eps', login_url='formatos_eps:dashboard', raise_exception=False)
def generar_pdf_masivo_view(request):
    """
    Recibe una lista de cédulas y genera un ZIP con los PDFs exitosos.
    """
    if request.method != 'POST':
        return redirect('formatos_eps:search')

    cedulas_raw = request.POST.get('cedulas', '')
    cedulas = _parsear_cedulas(cedulas_raw)

    if not cedulas:
        messages.error(request, 'No se detectaron cédulas válidas para procesar.')
        return redirect('formatos_eps:search')

    errores = []
    temp_dir = tempfile.gettempdir()
    zip_name = f"formularios_eps_masivo_{uuid.uuid4().hex[:8]}.zip"
    zip_path = os.path.join(temp_dir, zip_name)

    with zipfile.ZipFile(zip_path, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
        for cedula in cedulas:
            try:
                datos_empleado = find_row_by_cedula(cedula)
                if not datos_empleado:
                    errores.append(f"{cedula}: no encontrada")
                    continue

                datos_normalizados = _normalizar_datos_para_pdf(datos_empleado)
                nombre_archivo = generar_nombre_archivo_pdf(cedula, datos_normalizados.get('PRIMER_APELLIDO', ''))
                output_path = os.path.join(temp_dir, f"{uuid.uuid4().hex}_{nombre_archivo}")
                rellenar_pdf_empleado(datos_normalizados, output_path)
                zip_file.write(output_path, arcname=nombre_archivo)
            except Exception as e:
                errores.append(f"{cedula}: {str(e)}")

        if errores:
            zip_file.writestr('errores.txt', "\n".join(errores))

    if len(errores) == len(cedulas):
        messages.error(request, 'No se pudo generar ningún PDF. Revisa cédulas y configuración de EPS.')
        return redirect('formatos_eps:search')

    return FileResponse(
        open(zip_path, 'rb'),
        content_type='application/zip',
        as_attachment=True,
        filename=f"formularios_eps_{len(cedulas)}_cedulas.zip"
    )


@login_required(login_url='formatos_eps:login')
@permission_required('formatos_eps.ver_eps', login_url='formatos_eps:dashboard', raise_exception=False)
def generar_pdf_masivo_filtro_view(request):
    """
    Genera PDFs masivos aplicando filtros sobre Planta + Manipuladoras.
    """
    if request.method != 'POST':
        return redirect('formatos_eps:search')

    try:
        registros = _obtener_registros_unificados()
        filtrados = _filtrar_registros(registros, request.POST)
    except ConnectionError:
        messages.error(request, 'Error de conexión con Google Sheets.')
        return redirect('formatos_eps:search')
    except Exception as e:
        messages.error(request, f'Error al filtrar registros: {str(e)}')
        return redirect('formatos_eps:search')

    if not filtrados:
        messages.error(request, 'No se encontraron empleados con los filtros seleccionados.')
        return redirect('formatos_eps:search')

    errores = []
    generados = 0
    temp_dir = tempfile.gettempdir()
    zip_name = f"formularios_eps_filtros_{uuid.uuid4().hex[:8]}.zip"
    zip_path = os.path.join(temp_dir, zip_name)

    with zipfile.ZipFile(zip_path, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
        for row in filtrados:
            cedula = str(row.get('CEDULA', '')).strip()
            if not cedula:
                errores.append('SIN_CEDULA: registro omitido')
                continue

            try:
                datos_normalizados = _normalizar_datos_para_pdf(row)
                nombre_archivo = generar_nombre_archivo_pdf(cedula, datos_normalizados.get('PRIMER_APELLIDO', ''))
                output_path = os.path.join(temp_dir, f"{uuid.uuid4().hex}_{nombre_archivo}")
                rellenar_pdf_empleado(datos_normalizados, output_path)
                zip_file.write(output_path, arcname=nombre_archivo)
                generados += 1
            except Exception as e:
                errores.append(f"{cedula}: {str(e)}")

        resumen = [
            f"Total filtrados: {len(filtrados)}",
            f"PDF generados: {generados}",
            f"Errores: {len(errores)}",
        ]
        if errores:
            resumen.append('')
            resumen.append('Detalle de errores:')
            resumen.extend(errores)
        zip_file.writestr('resumen_generacion.txt', '\n'.join(resumen))

    if generados == 0:
        messages.error(request, 'No se pudo generar ningún PDF con los filtros seleccionados.')
        return redirect('formatos_eps:search')

    return FileResponse(
        open(zip_path, 'rb'),
        content_type='application/zip',
        as_attachment=True,
        filename=f"formularios_eps_filtrados_{generados}.zip"
    )
