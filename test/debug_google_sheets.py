import sys
import os

# Agregar path al proyecto
sys.path.append(os.path.join(os.getcwd(), 'formularios'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "formularios.settings")

import django
django.setup()

from formatos_eps.google_sheets import get_sheet_data

def debug_sheet(sheet_name):
    print(f"\n--- DEBUGGEANDO HOJA: {sheet_name} ---")
    try:
        data = get_sheet_data(sheet_name)
        if not data:
            print("No se encontraron datos.")
            return

        # Tomar el primer registro
        primer_registro = data[0]
        
        print(f"Total registros: {len(data)}")
        print("Claves (Columnas) encontradas en el primer registro:")
        
        keys = list(primer_registro.keys())
        for i, key in enumerate(keys):
            # Imprimir índice, clave y una muestra del valor
            val = primer_registro[key]
            print(f"[{i}] '{key}': '{val}'")
            
        # Verificar específicamente las columnas de interés
        interes = ['EMPRESA', 'AREA', 'PROGRAMA', 'PERTENECE']
        print("\nBusqueda especifica de palabras clave:")
        for key in keys:
            for palabra in interes:
                if palabra in key.upper():
                    print(f"!!! ENCONTRADO: '{key}' -> '{primer_registro[key]}'")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_sheet('Planta')
    debug_sheet('Manipuladoras')

