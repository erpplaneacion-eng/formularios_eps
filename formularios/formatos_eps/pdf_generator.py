"""
Módulo para generar PDFs de formularios EPS con datos de empleados
"""
import fitz  # PyMuPDF
import os
from django.conf import settings

# Ruta base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuración de formatos por EPS
CONFIGURACION_FORMATOS = {
    'COMFENALCO VALLE': {
        'archivo': 'formulario_de_afiliacion_eps_delagente_comfenalco_valle.pdf',
        'campos': {
            'CEDULA': {'x': 130, 'y': 181},
            'PRIMER_APELLIDO': {'x': 75, 'y': 163},
            'SEGUNDO_APELLIDO': {'x': 200, 'y': 163},
            'PRIMER_NOMBRE': {'x': 330, 'y': 163},
            'SEGUNDO_NOMBRE': {'x': 480, 'y': 163},
            'PAIS_NACIMIENTO': {'x': 155, 'y': 170, 'fontsize': 7},
            'DEPARTAMENTO_NACIMIENTO': {'x': 350, 'y': 195},
            'CIUDAD_NACIMIENTO': {'x': 380, 'y': 195},
        },
        'fecha_nacimiento': [
            {'x': 290, 'y': 200}, {'x': 310, 'y': 200}, # D
            {'x': 330, 'y': 200}, {'x': 350, 'y': 200}, # M
            {'x': 370, 'y': 200}, {'x': 390, 'y': 200}, {'x': 410, 'y': 200}, {'x': 435, 'y': 200} # Y
        ],
        'sexo': {
            '0': {'x': 302.5, 'y': 176.5},  # Masculino
            '1': {'x': 267.5, 'y': 176.5},  # Femenino
        },
        # Bloque 1: Datos del trámite (5 X's fijas)
        'datos_tramite': [
            {'x': 121, 'y': 120},   # Tipo de trámite
            {'x': 239, 'y': 110},  # Tipo de afiliación
            {'x': 333, 'y': 110},  # Régimen
            {'x': 395, 'y': 110},  # Tipo de afiliado
            {'x': 449, 'y': 110},  # Tipo de cotizante
        ],
        # Bloque 2: Administradora anterior (SURA)
        'administradora_anterior': {
            'valor': 'SURA',
            'x': 320, 'y': 229
        },
        # Bloque 3: Datos del empleador (8 campos)
        'datos_empleador': {
            'campo_variable': {'x': 90, 'y': 789},  # Columna F (Empresa/Area)
            'nit': {'valor': 'NIT', 'x': 238, 'y': 784},
            'numero_documento': {'valor': '123456789-55', 'x': 310, 'y': 789},
            'direccion': {'valor': 'calle 15 #26-101', 'x': 85, 'y': 603},
            'telefono': {'valor': '3164219523', 'x': 218, 'y': 604},
            'correo': {'valor': 'contratacionrh@vallesolidario.com', 'x': 292, 'y': 600, 'fontsize': 8},
            'ciudad': {'valor': 'YUMBO', 'x': 441, 'y': 598},
            'departamento': {'valor': 'VALLE DEL CAUCA', 'x': 491, 'y': 600, 'fontsize': 7},
        }
    },
    # Marcadores de posición para otras EPS (se configurarán a futuro)
    'SURA': None,
    'SOS': None,
    'SANITAS': None,
    'EMSSANAR': {
        'archivo': 'Formulario_Único_de_Afiliaciones_y_Registro_Novedades_EPS_EMSSANAR.pdf',
        'campos': {
            'CEDULA': {'x': 90, 'y': 161},
            'PRIMER_APELLIDO': {'x': 75, 'y': 153},
            'SEGUNDO_APELLIDO': {'x': 200, 'y': 153},
            'PRIMER_NOMBRE': {'x': 350, 'y': 153},
            'SEGUNDO_NOMBRE': {'x': 480, 'y': 153},
            'PAIS_NACIMIENTO': {'x': 505, 'y': 181},
            'DEPARTAMENTO_NACIMIENTO': {'x': 50, 'y': 200},
            'CIUDAD_NACIMIENTO': {'x': 130, 'y': 200},
        },
        'fecha_nacimiento': [
            {'x': 290, 'y': 200}, {'x': 310, 'y': 200}, # D
            {'x': 330, 'y': 200}, {'x': 350, 'y': 200}, # M
            {'x': 370, 'y': 200}, {'x': 390, 'y': 200}, {'x': 410, 'y': 200}, {'x': 435, 'y': 200} # Y
        ],
        'sexo': {
            '0': {'x': 312.5, 'y': 171.5},  # Masculino
            '1': {'x': 277.5, 'y': 171.5},  # Femenino
        },
        # Bloque 1: Datos del trámite (5 X's fijas)
        'datos_tramite': [
            {'x': 136, 'y': 115},   # Tipo de trámite
            {'x': 269, 'y': 100},  # Tipo de afiliación
            {'x': 393, 'y': 100},  # Régimen
            {'x': 465, 'y': 100},  # contribucion
            {'x': 100, 'y': 125},  # Tipo de afiliado
            {'x': 269, 'y': 125},  # Tipo de cotizante
        ],
        # Bloque 2: Administradora anterior (SURA)
        'administradora_anterior': {
            'valor': 'SURA',
            'x': 320, 'y': 229
        },
        # Bloque 3: Datos del empleador (8 campos)
        'datos_empleador': {
            'campo_variable': {'x': 90, 'y': 589},  # Columna F (Empresa/Area)
            'nit': {'valor': 'NIT', 'x': 238, 'y': 584},
            'numero_documento': {'valor': '123456789-55', 'x': 310, 'y': 589},
            'direccion': {'valor': 'calle 15 #26-101', 'x': 85, 'y': 603},
            'telefono': {'valor': '3164219523', 'x': 218, 'y': 604},
            'correo': {'valor': 'contratacionrh@vallesolidario.com', 'x': 292, 'y': 600, 'fontsize': 8},
            'ciudad': {'valor': 'YUMBO', 'x': 441, 'y': 598},
            'departamento': {'valor': 'VALLE DEL CAUCA', 'x': 491, 'y': 600, 'fontsize': 7},
        }
    },
    'SALUD TOTAL': None,
    'ASMET SALUD': None,
    'NUEVA EPS': None,
    'ASOCIACION MUTUAL SER EMPRESA SOLIDARIA DE SALUD EPS-S': None,
    'FAMISANAR': None,
    'COOSALUD': None,
    'ENTIDAD PROMOTORA DE SALUD MALLAMAS EPSI': None,
    'COMPENSAR': None,
    'A.I.C.': None
}

def convertir_fecha_yyyymmdd_a_ddmmyyyy(fecha_str):
    """
    Convierte fecha de formato YYYYMMDD a DDMMYYYY.

    Args:
        fecha_str (str): Fecha en formato YYYYMMDD (ej: "19900315")

    Returns:
        str: Fecha en formato DDMMYYYY (ej: "15031990")
    """
    if not fecha_str or len(fecha_str) != 8:
        return ''

    # Limpiar espacios
    fecha_str = str(fecha_str).strip()

    try:
        # YYYYMMDD -> DDMMYYYY
        yyyy = fecha_str[0:4]
        mm = fecha_str[4:6]
        dd = fecha_str[6:8]

        return dd + mm + yyyy
    except:
        return ''


def split_nombres(nombres_completos):
    """
    Divide los nombres en primer y segundo nombre.

    Args:
        nombres_completos (str): Nombres completos del empleado

    Returns:
        tuple: (primer_nombre, segundo_nombre)
    """
    if not nombres_completos:
        return ('', '')

    # Limpiar espacios extras
    nombres = nombres_completos.strip().split()

    if len(nombres) == 0:
        return ('', '')
    elif len(nombres) == 1:
        return (nombres[0], '')
    else:
        # Primer nombre y resto como segundo nombre
        primer_nombre = nombres[0]
        segundo_nombre = ' '.join(nombres[1:])
        return (primer_nombre, segundo_nombre)


def insertar_texto_en_pdf(page, texto, x, y, fontsize=10, color=(0, 0, 0)):
    """
    Inserta texto en una coordenada específica del PDF.

    Args:
        page: Página de PyMuPDF
        texto (str): Texto a insertar
        x (int/float): Coordenada X
        y (int/float): Coordenada Y
        fontsize (int): Tamaño de fuente
        color (tuple): Color RGB (0-1, 0-1, 0-1)
    """
    if not texto:
        return

    # Crear rectángulo para el texto (amplio para que no se corte)
    text_rect = fitz.Rect(x, y - fontsize, x + 200, y + fontsize)

    # Insertar texto
    page.insert_textbox(
        text_rect,
        str(texto),
        fontsize=fontsize,
        fontname="helv",  # Helvetica
        color=color,
        align=fitz.TEXT_ALIGN_LEFT
    )


def marcar_x_en_pdf(page, x, y, size=7, color=(0, 0, 0)):
    """
    Marca una X en una coordenada específica del PDF.

    Args:
        page: Página de PyMuPDF
        x (int/float): Coordenada X
        y (int/float): Coordenada Y
        size (int): Tamaño de la X
        color (tuple): Color RGB (0-1, 0-1, 0-1)
    """
    # Dibujar línea diagonal de arriba-izquierda a abajo-derecha
    page.draw_line(
        (x - size/2, y - size/2),
        (x + size/2, y + size/2),
        color=color,
        width=1.5
    )

    # Dibujar línea diagonal de arriba-derecha a abajo-izquierda
    page.draw_line(
        (x + size/2, y - size/2),
        (x - size/2, y + size/2),
        color=color,
        width=1.5
    )


def insertar_fecha_nacimiento(page, fecha_yyyymmdd, coordenadas):
    """
    Inserta la fecha de nacimiento distribuyendo cada dígito en su coordenada.

    Args:
        page: Página de PyMuPDF
        fecha_yyyymmdd (str): Fecha en formato YYYYMMDD
        coordenadas (list): Lista de diccionarios con 'x' y 'y' para cada dígito
    """
    # Convertir a DDMMYYYY
    fecha_ddmmyyyy = convertir_fecha_yyyymmdd_a_ddmmyyyy(fecha_yyyymmdd)

    if not fecha_ddmmyyyy or len(fecha_ddmmyyyy) != 8:
        return

    # Validar que tengamos coordenadas para los 8 dígitos
    if len(coordenadas) < 8:
        return

    # Insertar cada dígito en su coordenada
    for i, digito in enumerate(fecha_ddmmyyyy):
        coords = coordenadas[i]
        insertar_texto_en_pdf(page, digito, coords['x'], coords['y'], fontsize=10)


def rellenar_pdf_empleado(datos_empleado, output_path):
    """
    Rellena el PDF del formulario EPS con los datos del empleado.
    Selecciona automáticamente el formato basado en la EPS del empleado.

    Args:
        datos_empleado (dict): Diccionario con los datos del empleado
            Debe contener: CEDULA, PRIMER_APELLIDO, SEGUNDO_APELLIDO, NOMBRES, EPS
        output_path (str): Ruta donde guardar el PDF generado

    Returns:
        str: Ruta del PDF generado

    Raises:
        FileNotFoundError: Si no se encuentra el PDF template
        ValueError: Si la EPS no está configurada o soportada
        Exception: Si hay error al generar el PDF
    """
    
    # 1. Identificar la EPS
    nombre_eps = datos_empleado.get('EPS', '').strip().upper()
    
    if not nombre_eps:
        raise ValueError("El empleado no tiene una EPS asignada en los datos.")

    # 2. Obtener configuración
    config = CONFIGURACION_FORMATOS.get(nombre_eps)

    if config is None:
        raise ValueError(f"No existe configuración de formulario para la EPS: {nombre_eps}")

    archivo_template = config.get('archivo')
    if not archivo_template:
         raise ValueError(f"La configuración de la EPS {nombre_eps} está incompleta (falta archivo).")

    pdf_template_path = os.path.join(BASE_DIR, 'formatos', archivo_template)

    # Verificar que existe el template
    if not os.path.exists(pdf_template_path):
        raise FileNotFoundError(f"No se encuentra el archivo de plantilla: {pdf_template_path}")

    try:
        # Abrir el PDF template
        doc = fitz.open(pdf_template_path)

        # Obtener la primera página (asumimos que el formulario está en página 1)
        page = doc[0]

        # Extraer datos del empleado
        cedula = datos_empleado.get('CEDULA', '')
        primer_apellido = datos_empleado.get('PRIMER_APELLIDO', '')
        segundo_apellido = datos_empleado.get('SEGUNDO_APELLIDO', '')
        nombres_completos = datos_empleado.get('NOMBRES', '')
        fecha_nacimiento = datos_empleado.get('FECHA_NACIMIENTO', '')
        pais_nacimiento = datos_empleado.get('PAIS_NACIMIENTO', '')
        codigo_sexo = datos_empleado.get('CODIGO_SEXO', '')
        departamento_nacimiento = datos_empleado.get('DEPARTAMENTO_NACIMIENTO', '')
        ciudad_nacimiento = datos_empleado.get('CIUDAD_NACIMIENTO', '')

        # Dividir nombres
        primer_nombre, segundo_nombre = split_nombres(nombres_completos)

        # Obtener mapas de coordenadas de la configuración
        mapa_campos = config.get('campos', {})
        mapa_fecha = config.get('fecha_nacimiento', [])
        mapa_sexo = config.get('sexo', {})

        # -- INSERCIÓN DE DATOS GENÉRICOS --
        
        # Mapeo de variables locales a claves en la configuración
        campos_simples = {
            'CEDULA': cedula,
            'PRIMER_APELLIDO': primer_apellido,
            'SEGUNDO_APELLIDO': segundo_apellido,
            'PRIMER_NOMBRE': primer_nombre,
            'SEGUNDO_NOMBRE': segundo_nombre,
            'PAIS_NACIMIENTO': pais_nacimiento,
            'DEPARTAMENTO_NACIMIENTO': departamento_nacimiento,
            'CIUDAD_NACIMIENTO': ciudad_nacimiento,
        }

        for clave_campo, valor in campos_simples.items():
            if valor and clave_campo in mapa_campos:
                coords = mapa_campos[clave_campo]
                # Ajustar tamaño de fuente para ciertos campos si es necesario (ej: depto)
                size = 8 if 'DEPARTAMENTO' in clave_campo else 10
                insertar_texto_en_pdf(page, valor, coords['x'], coords['y'], fontsize=size)

        # -- INSERCIONES ESPECIALES --

        # Insertar FECHA DE NACIMIENTO
        if fecha_nacimiento and mapa_fecha:
            insertar_fecha_nacimiento(page, fecha_nacimiento, mapa_fecha)

        # Marcar SEXO
        if codigo_sexo and str(codigo_sexo) in mapa_sexo:
            coords = mapa_sexo[str(codigo_sexo)]
            marcar_x_en_pdf(page, coords['x'], coords['y'], size=7)

        # -- NUEVOS BLOQUES --

        # 1. Datos del trámite (X's fijas)
        datos_tramite = config.get('datos_tramite', [])
        for coords in datos_tramite:
            marcar_x_en_pdf(page, coords['x'], coords['y'], size=7)

        # 2. Administradora anterior
        admin_anterior = config.get('administradora_anterior')
        if admin_anterior:
            insertar_texto_en_pdf(page, admin_anterior['valor'], admin_anterior['x'], admin_anterior['y'])

        # 3. Datos del empleador
        datos_empleador = config.get('datos_empleador', {})
        if datos_empleador:
            # Obtener valor variable según la hoja de origen
            origen = datos_empleado.get('_origen_hoja', '')
            valor_empresa = ''

            if origen == 'Planta':
                valor_empresa = datos_empleado.get('EMPRESA', '')
            elif origen == 'Manipuladoras':
                valor_empresa = datos_empleado.get('PROGRAMA AL QUE PERTENECE', '')
            
            # Fallbacks si no se encontró valor o no hay origen definido
            if not valor_empresa:
                valor_empresa = datos_empleado.get('EMPRESA')
            if not valor_empresa:
                valor_empresa = datos_empleado.get('AREA', '')
            
            # Iterar sobre los campos configurados
            for key, info in datos_empleador.items():
                valor = ''
                if key == 'campo_variable':
                    valor = valor_empresa
                elif 'valor' in info:
                    valor = info['valor']
                
                if valor:
                    print(f"DEBUG: Insertando campo '{key}' -> Valor: '{valor}' en ({info['x']}, {info['y']})")
                    text_fontsize = info.get('fontsize', 10) # Obtener fontsize de la configuración, default 10
                    insertar_texto_en_pdf(page, valor, info['x'], info['y'], fontsize=text_fontsize)

        # Guardar el PDF generado
        doc.save(output_path)
        doc.close()

        return output_path

    except Exception as e:
        raise Exception(f"Error al generar el PDF para {nombre_eps}: {str(e)}")


def generar_nombre_archivo_pdf(cedula):
    """
    Genera un nombre de archivo único para el PDF.

    Args:
        cedula (str): Número de cédula del empleado

    Returns:
        str: Nombre del archivo (ej: "formulario_1234567890.pdf")
    """
    return f"formulario_eps_{cedula}.pdf"


# Función de prueba
if __name__ == "__main__":
    # Datos de prueba
    datos_prueba = {
        'CEDULA': '1234567890',
        'PRIMER_APELLIDO': 'GARCÍA',
        'SEGUNDO_APELLIDO': 'LÓPEZ',
        'NOMBRES': 'JUAN CARLOS',
    }

    output_test = "test_formulario_generado.pdf"

    try:
        resultado = rellenar_pdf_empleado(datos_prueba, output_test)
        print(f"✓ PDF generado exitosamente: {resultado}")
    except Exception as e:
        print(f"✗ Error: {e}")
