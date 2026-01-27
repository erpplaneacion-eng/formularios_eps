import sys
import os

# Agregar path al proyecto
sys.path.append(os.path.join(os.getcwd(), 'formularios'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "formularios.settings")

import django
django.setup()

from formatos_eps.pdf_generator import rellenar_pdf_empleado

print("=== PRUEBA DE GENERACION CON DATOS REALES ===")

# CASO 1: Empleado de Planta
datos_planta = {
    'CEDULA': '1116723084',
    'PRIMER_APELLIDO': 'ACOSTA',
    'SEGUNDO_APELLIDO': 'GRACIA',
    'NOMBRES': 'JUAN MANUEL',
    'EPS': 'COMFENALCO VALLE',
    'EMPRESA': 'CORPORACION TEST PLANTA',  # Valor prueba
    '_origen_hoja': 'Planta'
}

try:
    path = rellenar_pdf_empleado(datos_planta, 'test_planta.pdf')
    print(f"PDF Planta generado: {path}")
except Exception as e:
    print(f"Error Planta: {e}")


# CASO 2: Manipuladora
datos_manipuladora = {
    'CEDULA': '1118283741',
    'PRIMER_APELLIDO': 'AGREDO',
    'SEGUNDO_APELLIDO': 'MUÑOZ',
    'NOMBRES': 'LAURA MILENA',
    'EPS': 'COMFENALCO VALLE',
    'PROGRAMA AL QUE PERTENECE': 'UT YUMBO TEST', # Valor prueba
    '_origen_hoja': 'Manipuladoras'
}

try:
    path = rellenar_pdf_empleado(datos_manipuladora, 'test_manipuladora.pdf')
    print(f"PDF Manipuladora generado: {path}")
except Exception as e:
    print(f"Error Manipuladora: {e}")
