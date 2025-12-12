"""
Prueba rápida para generar PDF de empleado con COMFENALCO VALLE
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

def generar_pdf_comfenalco():
    """Genera PDF de prueba con empleado COMFENALCO VALLE"""

    # Usar cédula de ejemplo de COMFENALCO VALLE
    # Opción 1: Planta
    cedula = "94540592"

    # Opción 2: Manipuladoras (descomenta para usar)
    # cedula = "29974569"

    print("=" * 80)
    print(f"GENERANDO PDF PARA CÉDULA: {cedula}")
    print("=" * 80)

    # 1. Buscar empleado
    print(f"\n1️⃣ Buscando empleado...")
    datos = find_row_by_cedula(cedula)

    if not datos:
        print(f"❌ No se encontró empleado con cédula {cedula}")
        return

    print(f"✅ Empleado encontrado")
    print(f"   Nombre: {datos.get('NOMBRES')} {datos.get('PRIMER_APELLIDO')} {datos.get('SEGUNDO_APELLIDO')}")
    print(f"   EPS: {datos.get('EPS')}")
    print(f"   Origen: {datos.get('_origen_hoja')}")

    # 2. Mostrar campo variable
    print(f"\n2️⃣ Campo Variable (Empresa/Programa):")
    origen = datos.get('_origen_hoja', '')

    if origen == 'Planta':
        valor = datos.get('EMPRESA', '')
        print(f"   Empresa: {valor}")
        print(f"   Área: {datos.get('AREA', '')}")
    elif origen == 'Manipuladoras':
        valor = datos.get('PROGRAMA AL QUE PERTENECE', '')
        print(f"   Programa: {valor}")
        print(f"   Área: {datos.get('AREA', '')}")

    # 3. Generar PDF
    print(f"\n3️⃣ Generando PDF...")
    output_path = f"formulario_eps_{cedula}.pdf"

    try:
        print("\n   📄 Logs de inserción de campos:")
        print("   " + "-" * 76)

        resultado = rellenar_pdf_empleado(datos, output_path)

        print("   " + "-" * 76)
        print(f"\n✅ PDF generado exitosamente!")
        print(f"   📁 Ubicación: {os.path.abspath(output_path)}")
        print(f"\n🔍 IMPORTANTE: Revisa el PDF y verifica:")
        print(f"   - El campo 'Empresa/Programa' aparece en coordenadas (120, 590)")
        print(f"   - El valor esperado es: '{valor}'")
        print(f"\n💡 Abre el PDF con Adobe Reader para mejor visualización")

    except Exception as e:
        print(f"❌ Error al generar PDF: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 80)

if __name__ == "__main__":
    generar_pdf_comfenalco()
