"""
Script de diagnóstico para verificar columnas en Google Sheets
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'formularios'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formularios.settings')
django.setup()

from formatos_eps.google_sheets import get_sheet_data

def diagnosticar_columnas():
    """Muestra todas las columnas disponibles en ambas hojas"""

    print("=" * 80)
    print("DIAGNÓSTICO DE COLUMNAS EN GOOGLE SHEETS")
    print("=" * 80)

    # Diagnosticar hoja Planta
    print("\n📊 HOJA: Planta")
    print("-" * 80)
    try:
        planta_data = get_sheet_data('Planta')
        if planta_data:
            print(f"Total registros: {len(planta_data)}")
            print("\nColumnas disponibles:")
            columnas = list(planta_data[0].keys())
            for i, col in enumerate(columnas, 1):
                print(f"  {i:2}. {col}")

            # Mostrar primer registro como ejemplo
            print("\n📝 Ejemplo de primer registro:")
            primer_registro = planta_data[0]
            for key, value in primer_registro.items():
                if value:  # Solo mostrar si tiene valor
                    print(f"  {key}: {value}")
        else:
            print("⚠️ No hay datos en la hoja Planta")
    except Exception as e:
        print(f"❌ Error al leer hoja Planta: {e}")

    # Diagnosticar hoja Manipuladoras
    print("\n" + "=" * 80)
    print("\n📊 HOJA: Manipuladoras")
    print("-" * 80)
    try:
        manipuladoras_data = get_sheet_data('Manipuladoras')
        if manipuladoras_data:
            print(f"Total registros: {len(manipuladoras_data)}")
            print("\nColumnas disponibles:")
            columnas = list(manipuladoras_data[0].keys())
            for i, col in enumerate(columnas, 1):
                print(f"  {i:2}. {col}")

            # Mostrar primer registro como ejemplo
            print("\n📝 Ejemplo de primer registro:")
            primer_registro = manipuladoras_data[0]
            for key, value in primer_registro.items():
                if value:  # Solo mostrar si tiene valor
                    print(f"  {key}: {value}")
        else:
            print("⚠️ No hay datos en la hoja Manipuladoras")
    except Exception as e:
        print(f"❌ Error al leer hoja Manipuladoras: {e}")

    # Análisis para el campo variable
    print("\n" + "=" * 80)
    print("\n🔍 ANÁLISIS DEL CAMPO VARIABLE (Empresa/Área)")
    print("-" * 80)
    print("\nEl código busca en este orden:")
    print("  1. Si origen='Planta' → Columna 'EMPRESA'")
    print("  2. Si origen='Manipuladoras' → Columna 'PROGRAMA AL QUE PERTENECE'")
    print("  3. Fallback → Columna 'EMPRESA' o 'AREA'")

    # Verificar si existen estas columnas
    print("\n✓ Verificación de columnas:")
    if planta_data:
        columnas_planta = list(planta_data[0].keys())
        print("\n  En Planta:")
        print(f"    - 'EMPRESA' existe: {'EMPRESA' in columnas_planta}")
        print(f"    - 'AREA' existe: {'AREA' in columnas_planta}")

        # Buscar columnas similares
        cols_empresa = [c for c in columnas_planta if 'EMPRES' in c.upper() or 'AREA' in c.upper()]
        if cols_empresa:
            print(f"    - Columnas relacionadas: {cols_empresa}")

    if manipuladoras_data:
        columnas_manip = list(manipuladoras_data[0].keys())
        print("\n  En Manipuladoras:")
        print(f"    - 'PROGRAMA AL QUE PERTENECE' existe: {'PROGRAMA AL QUE PERTENECE' in columnas_manip}")

        # Buscar columnas similares
        cols_programa = [c for c in columnas_manip if 'PROGRAMA' in c.upper() or 'AREA' in c.upper()]
        if cols_programa:
            print(f"    - Columnas relacionadas: {cols_programa}")

    print("\n" + "=" * 80)
    print("✅ Diagnóstico completado")
    print("=" * 80)

if __name__ == "__main__":
    try:
        diagnosticar_columnas()
    except Exception as e:
        print(f"\n❌ Error general: {e}")
        import traceback
        traceback.print_exc()
