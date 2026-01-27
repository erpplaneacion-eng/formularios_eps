
import os
import sys
import django
from django.conf import settings

# Configure Django settings manually
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Add the 'formularios' directory to sys.path so we can import 'formatos_eps'
sys.path.append(os.path.join(BASE_DIR, 'formularios'))

if not settings.configured:
    settings.configure(
        BASE_DIR=BASE_DIR,
        INSTALLED_APPS=[
            'formatos_eps',
        ],
    )
    django.setup()

# Import directly from the app
from formatos_eps.pdf_generator import rellenar_pdf_empleado

def test_pdf_generation():
    # Mock data for the provided cedula based on typical structure
    # We are simulating what would come from Google Sheets
    mock_employee_data = {
        'CEDULA': '94540592',
        'PRIMER_APELLIDO': 'PEREZ',
        'SEGUNDO_APELLIDO': 'LOPEZ',
        'NOMBRES': 'JUAN CARLOS',
        'FECHA_NACIMIENTO': '19850520',
        'PAIS_NACIMIENTO': 'COLOMBIA',
        'CODIGO_SEXO': '0', # Masculino
        'DEPARTAMENTO_NACIMIENTO': 'VALLE DEL CAUCA',
        'CIUDAD_NACIMIENTO': 'CALI',
        'EPS': 'COMFENALCO VALLE' # Crucial for the test
    }

    output_path = os.path.join(BASE_DIR, 'test_output_94540592.pdf')

    try:
        print(f"Testing PDF generation for cedula: {mock_employee_data['CEDULA']} with EPS: {mock_employee_data['EPS']}")
        result_path = rellenar_pdf_empleado(mock_employee_data, output_path)
        print(f"SUCCESS: PDF generated at {result_path}")
    except Exception as e:
        print(f"FAILURE: {str(e)}")

if __name__ == "__main__":
    test_pdf_generation()
