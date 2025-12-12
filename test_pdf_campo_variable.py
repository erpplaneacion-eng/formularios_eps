"""
Script de prueba para verificar el campo_variable en PDF
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'formularios'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formularios.settings')
django.setup()

from formatos_eps.google_sheets import find_row_by_cedula
from formatos_eps.pdf_generator import rellenar_pdf_empleado

def test_campo_variable():
    """Prueba la generación del PDF con el campo variable"""

    print("=" * 80)
    print("PRUEBA DE GENERACIÓN PDF - CAMPO VARIABLE")
    print("=" * 80)

    # Usar la cédula del ejemplo de Planta
    cedula_planta = "1116723084"
    # Usar la cédula del ejemplo de Manipuladoras
    cedula_manipuladoras = "1118283741"

    for i, cedula in enumerate([cedula_planta, cedula_manipuladoras], 1):
        print(f"\n{'=' * 80}")
        print(f"PRUEBA {i}: Cédula {cedula}")
        print("=" * 80)

        # 1. Buscar empleado
        print(f"\n1️⃣ Buscando empleado con cédula {cedula}...")
        try:
            datos = find_row_by_cedula(cedula)

            if not datos:
                print(f"❌ No se encontró empleado con cédula {cedula}")
                continue

            print(f"✅ Empleado encontrado")

            # 2. Mostrar datos relevantes
            print("\n2️⃣ Datos del empleado:")
            print(f"  - Nombre: {datos.get('NOMBRES')} {datos.get('PRIMER_APELLIDO')} {datos.get('SEGUNDO_APELLIDO')}")
            print(f"  - Origen: {datos.get('_origen_hoja')}")
            print(f"  - EPS: {datos.get('EPS')}")

            # 3. Mostrar campo variable
            print("\n3️⃣ Campo Variable (Empresa/Área):")
            origen = datos.get('_origen_hoja', '')

            if origen == 'Planta':
                valor_empresa = datos.get('EMPRESA', '')
                print(f"  - Origen: Planta")
                print(f"  - Columna 'EMPRESA': '{valor_empresa}'")
                print(f"  - Columna 'AREA': '{datos.get('AREA', '')}'")
            elif origen == 'Manipuladoras':
                valor_empresa = datos.get('PROGRAMA AL QUE PERTENECE', '')
                print(f"  - Origen: Manipuladoras")
                print(f"  - Columna 'PROGRAMA AL QUE PERTENECE': '{valor_empresa}'")
                print(f"  - Columna 'AREA': '{datos.get('AREA', '')}'")
            else:
                print(f"  - ⚠️ Origen no definido")
                valor_empresa = datos.get('EMPRESA', '') or datos.get('AREA', '')
                print(f"  - Valor detectado: '{valor_empresa}'")

            # 4. Verificar si la EPS está configurada
            eps = datos.get('EPS', '').strip().upper()
            print(f"\n4️⃣ Verificación EPS:")
            print(f"  - EPS detectada: '{eps}'")

            # Solo COMFENALCO VALLE está configurado
            if eps != 'COMFENALCO VALLE':
                print(f"  - ⚠️ La EPS '{eps}' no tiene plantilla PDF configurada")
                print(f"  - ℹ️ Solo 'COMFENALCO VALLE' está disponible")
                print(f"\n  💡 Para probar, busca un empleado con EPS = 'COMFENALCO VALLE'")
                continue

            print(f"  - ✅ EPS configurada correctamente")

            # 5. Generar PDF
            print(f"\n5️⃣ Generando PDF...")
            output_path = f"test_pdf_{cedula}.pdf"

            try:
                resultado = rellenar_pdf_empleado(datos, output_path)
                print(f"✅ PDF generado exitosamente: {resultado}")
                print(f"\n  📄 Verifica el archivo: {os.path.abspath(output_path)}")
                print(f"  🔍 Revisa si el campo 'campo_variable' aparece en coordenadas (120, 590)")
            except Exception as e:
                print(f"❌ Error al generar PDF: {e}")
                import traceback
                traceback.print_exc()

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 80)
    print("✅ Prueba completada")
    print("=" * 80)

    # Buscar empleados con COMFENALCO VALLE
    print("\n" + "=" * 80)
    print("🔍 BÚSQUEDA DE EMPLEADOS CON COMFENALCO VALLE")
    print("=" * 80)

    try:
        from formatos_eps.google_sheets import get_sheet_data

        print("\nBuscando en hoja 'Planta'...")
        planta_data = get_sheet_data('Planta')
        comfenalco_planta = [r for r in planta_data if r.get('EPS', '').strip().upper() == 'COMFENALCO VALLE']

        if comfenalco_planta:
            print(f"  ✅ Encontrados {len(comfenalco_planta)} empleados con COMFENALCO VALLE")
            print(f"\n  📝 Ejemplos (primeros 5):")
            for i, emp in enumerate(comfenalco_planta[:5], 1):
                print(f"    {i}. Cédula: {emp.get('CEDULA')} - {emp.get('NOMBRES')} {emp.get('PRIMER_APELLIDO')}")
                print(f"       Empresa: {emp.get('EMPRESA')} - Área: {emp.get('AREA')}")
        else:
            print("  ⚠️ No se encontraron empleados con COMFENALCO VALLE en Planta")

        print("\nBuscando en hoja 'Manipuladoras'...")
        manip_data = get_sheet_data('Manipuladoras')
        comfenalco_manip = [r for r in manip_data if r.get('EPS', '').strip().upper() == 'COMFENALCO VALLE']

        if comfenalco_manip:
            print(f"  ✅ Encontrados {len(comfenalco_manip)} empleados con COMFENALCO VALLE")
            print(f"\n  📝 Ejemplos (primeros 5):")
            for i, emp in enumerate(comfenalco_manip[:5], 1):
                print(f"    {i}. Cédula: {emp.get('CEDULA')} - {emp.get('NOMBRES')} {emp.get('PRIMER_APELLIDO')}")
                print(f"       Programa: {emp.get('PROGRAMA AL QUE PERTENECE')} - Área: {emp.get('AREA')}")
        else:
            print("  ⚠️ No se encontraron empleados con COMFENALCO VALLE en Manipuladoras")

    except Exception as e:
        print(f"❌ Error en búsqueda: {e}")

if __name__ == "__main__":
    test_campo_variable()
