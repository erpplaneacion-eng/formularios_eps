"""
Módulo para generar PDFs de formularios EPS con datos de empleados
"""
import fitz  # PyMuPDF
import os
from django.conf import settings

# Ruta base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuración de NITs por Empresa
NITS_EMPRESAS = {
    "CORPORACION": "805.029.170-0",
    "CONSORCIO 2025": "901945753-1",
    "UT ALIMENTANDO YUMBO 2025": "901979218-9",
    "UT BUGA 2025": "901901689-9",
    "UT YUMBO 2025": "901909200-8",
    "CONSORCIO 2026": "902021552-6",
    "UT ALIMENTANDO YUMBO 2026": "902027434-2",
    "UT BUGA 2026": "902023530-3",    
}

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
            'PAIS_NACIMIENTO': {'x': 510, 'y': 181, 'fontsize': 7},
            'DEPARTAMENTO_NACIMIENTO': {'x': 55, 'y': 200, 'fontsize': 6},
            'CIUDAD_NACIMIENTO': {'x': 130, 'y': 200},
            'PAIS_NACIMIENTO_2': {'x': 460, 'y': 181, 'fontsize': 7}, # TODO: Ajustar coordenadas (Duplicado)
            'TIPO_DOCUMENTO_CC': {'x': 102, 'y': 177.5, 'fontsize': 9}, # TODO: Ajustar coordenadas (Constante CC)
            'AFP': {'x': 460, 'y': 229, 'fontsize': 8}, 
            'SALARIO_BASICO': {'x': 55, 'y': 245, 'fontsize': 8}, 
            'CORREO_ELECTRONICO': {'x': 55, 'y': 255, 'fontsize': 8},
            'DIRECCION_RESIDENCIA': {'x': 175, 'y': 245, 'fontsize': 6}, 
            'TELEFONO_MOVIL': {'x': 485, 'y': 235, 'fontsize': 6}, 
            'BARRIO': {'x': 368, 'y': 255, 'fontsize': 5}, 
            'CIUDAD_RESIDENCIA': {'x': 235, 'y': 255, 'fontsize': 8}, 
            'DEPARTAMENTO_NACIMIENTO2': {'x': 470, 'y': 255, 'fontsize': 8, 'page': 0},
        },
        'fecha_nacimiento': [
            {'x': 290, 'y': 200}, {'x': 310, 'y': 200}, # D
            {'x': 330, 'y': 200}, {'x': 350, 'y': 200}, # M
            {'x': 370, 'y': 200}, {'x': 390, 'y': 200}, {'x': 410, 'y': 200}, {'x': 435, 'y': 200} # Y
        ],
        'fecha_nacimiento2': [
             {'x': 487, 'y': 728, 'page': 0}, {'x': 496, 'y': 728, 'page': 0}, # D
             {'x': 508, 'y': 728, 'page': 0}, {'x': 518, 'y': 728, 'page': 0}, # M
             {'x': 529, 'y': 728, 'page': 0}, {'x': 539, 'y': 728, 'page': 0}, {'x': 549, 'y': 728, 'page': 0}, {'x': 559, 'y': 728, 'page': 0} # Y
        ],
        'sexo': {
            '0': {'x': 302.5, 'y': 176.5},  # Masculino
            '1': {'x': 267.5, 'y': 176.5},  # Femenino
        },
        'sexo_2': { # Campo de sexo duplicado
            '0': {'x': 340, 'y': 176.5}, # TODO: Ajustar coordenadas para Masculino
            '1': {'x': 326.5, 'y': 176.5}, # TODO: Ajustar coordenadas para Femenino
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
            'campo_variable': {'x': 90, 'y': 588},  # Columna F (Empresa/Area)
            'nit': {'valor': 'NIT', 'x': 235, 'y': 588},
            'numero_documento': {'valor': '123456789-55', 'x': 310, 'y': 588},
            'direccion': {'valor': 'calle 15 #26-101', 'x': 85, 'y': 603},
            'telefono': {'valor': '3164219523', 'x': 218, 'y': 603},
            'correo': {'valor': 'contratacionrh@vallesolidario.com', 'x': 292, 'y': 603, 'fontsize': 8},
            'ciudad': {'valor': 'YUMBO', 'x': 441, 'y': 603},
            'departamento': {'valor': 'VALLE DEL CAUCA', 'x': 491, 'y': 603, 'fontsize': 7},
        }
    },
    # Marcadores de posición para otras EPS (se configurarán a futuro)
    'SURA': None,
    'SOS': {
        'archivo': 'Anexo-Formulario-EPS_SOS_PBS-2025-Oficio.pdf',
        'campos': {
            'CEDULA': {'x': 195, 'y': 232},
            'PRIMER_APELLIDO': {'x': 75, 'y': 210},
            'SEGUNDO_APELLIDO': {'x': 215, 'y': 210},
            'PRIMER_NOMBRE': {'x': 330, 'y': 210},
            'SEGUNDO_NOMBRE': {'x': 460, 'y': 210},
            'PAIS_NACIMIENTO': {'x': 170, 'y': 250, 'fontsize': 7},
            'DEPARTAMENTO_NACIMIENTO': {'x': 299, 'y': 250, 'fontsize': 5},
            'CIUDAD_NACIMIENTO': {'x': 406, 'y': 250, 'fontsize': 7},
            'AFP': {'x': 195, 'y': 322, 'fontsize': 8}, 
            'SALARIO_BASICO': {'x': 331, 'y': 322, 'fontsize': 8}, 
            'CORREO_ELECTRONICO': {'x': 432, 'y': 340, 'fontsize': 8},
            'DIRECCION_RESIDENCIA': {'x': 60, 'y': 340, 'fontsize': 8}, 
            'TELEFONO_MOVIL': {'x': 340, 'y': 334, 'fontsize': 8}, 
            'BARRIO': {'x': 253, 'y': 355, 'fontsize': 6}, 
            'CIUDAD_RESIDENCIA': {'x': 190, 'y': 355, 'fontsize': 8}, 
            'DEPARTAMENTO_NACIMIENTO2': {'x': 40, 'y': 355, 'fontsize': 8, 'page': 0},
            'CEDULA_PAGINA_3': {'x': 268, 'y': 736, 'fontsize': 10, 'page': 2}, # TODO: Ajustar coordenadas
        },
        'fecha_nacimiento': [
            {'x': 515, 'y': 250}, {'x': 521, 'y': 250}, # D
            {'x': 527, 'y': 250}, {'x': 533, 'y': 250}, # M
            {'x': 539, 'y': 250}, {'x': 545, 'y': 250}, {'x': 551, 'y': 250}, {'x': 557, 'y': 250} # Y
        ],
        'fecha_nacimiento2': [
             {'x': 178, 'y': 300, 'page': 1}, {'x': 186, 'y': 300, 'page': 1}, # D
             {'x': 196, 'y': 300, 'page': 1}, {'x': 202, 'y': 300, 'page': 1}, # M
             {'x': 212, 'y': 300, 'page': 1}, {'x': 218, 'y': 300, 'page': 1}, {'x': 226, 'y': 300, 'page': 1}, {'x': 232, 'y': 300, 'page': 1} # Y
        ],
        'sexo': {
            '0': {'x': 394, 'y': 227, 'fontsize': 4},  # Masculino
            '1': {'x': 335, 'y': 227, 'fontsize': 4},  # Femenino
        },
        'sexo_identificacion': {
            '0': {'x': 524, 'y': 217, 'fontsize': 4},  # Masculino
            '1': {'x': 488, 'y': 217, 'fontsize': 4},  # Femenino
        },
        # Bloque 1: Datos del trámite (5 X's fijas)
        'datos_tramite': [
            {'x': 92, 'y': 147},   # Tipo de trámite
            {'x': 342, 'y': 130},  # Tipo de afiliación
            {'x': 459, 'y': 136},  # Régimen
            {'x': 549, 'y': 146},  # contribucion
            {'x': 118, 'y': 160},  # Tipo de afiliado
            {'x': 293, 'y': 168, 'fontsize': 4},  # Tipo de cotizante
            # {'x': 491, 'y': 348, 'fontsize': 4},  # zona
            {'x': 290, 'y': 686, 'page': 2}, # TODO: Ajustar coordenadas para la X fija en pag 3
        ],
        # Bloque 2: Administradora anterior (SURA)
        'administradora_anterior': {
            'valor': 'SURA',
            'x': 60, 'y': 322
        },
        # Bloque 3: Datos del empleador (8 campos)
        'datos_empleador': {
            'campo_variable': {'x': 70, 'y': 895},  # Columna F (Empresa/Area)
            'nit': {'valor': 'NIT', 'x': 260, 'y': 895},
            'numero_documento': {'valor': '123456789-55', 'x': 315, 'y': 895},
            'direccion': {'valor': 'calle 15 #26-101', 'x': 28, 'y': 915},
            'telefono': {'valor': '3164219523', 'x': 113, 'y': 915},
            'correo': {'valor': 'contratacionrh@vallesolidario.com', 'x': 182, 'y': 915, 'fontsize': 6},
            'ciudad': {'valor': 'YUMBO', 'x': 457, 'y': 915},
            'departamento': {'valor': 'VALLE DEL CAUCA', 'x': 310, 'y': 915, 'fontsize': 7},
            'pais': {'valor': 'COLOMBIA', 'x': 60, 'y': 250, 'fontsize': 8},
            'tipo_documento': {'valor': 'CC', 'x': 75, 'y': 232, 'fontsize': 8},
        }
    },
    'SANITAS': {
        'archivo': 'Formulario-Afiliacion-EPS-Sanitas-2025.pdf',
        'campos': {
            'CEDULA': {'x': 175, 'y': 175},
            'PRIMER_APELLIDO': {'x': 45, 'y': 154},
            'SEGUNDO_APELLIDO': {'x': 185, 'y': 154},
            'PRIMER_NOMBRE': {'x': 330, 'y': 154},
            'SEGUNDO_NOMBRE': {'x': 460, 'y': 154},
            'PAIS_NACIMIENTO': {'x': 170, 'y': 195, 'fontsize': 10},
            'DEPARTAMENTO_NACIMIENTO': {'x': 240, 'y': 195, 'fontsize': 10},
            'CIUDAD_NACIMIENTO': {'x': 45, 'y': 195, 'fontsize': 10},
            'AFP': {'x': 230, 'y': 256, 'fontsize': 10}, 
            'SALARIO_BASICO': {'x': 360, 'y': 256, 'fontsize': 10}, 
            'CORREO_ELECTRONICO': {'x': 200, 'y': 293, 'fontsize': 10},
            'DIRECCION_RESIDENCIA': {'x': 90, 'y': 276, 'fontsize': 10}, 
            'TELEFONO_MOVIL': {'x': 57, 'y': 295, 'fontsize': 10}, 
            'BARRIO': {'x': 325, 'y': 310, 'fontsize': 5}, 
            'CIUDAD_RESIDENCIA': {'x': 360, 'y': 195, 'fontsize': 10}, 
            'DEPARTAMENTO_NACIMIENTO2': {'x': 48, 'y': 310, 'fontsize': 10, 'page': 0},
            'CIUDAD_RESIDENCIA_3': {'x': 215, 'y': 310, 'fontsize': 10}, 
            
        },
        'fecha_nacimiento': [
            {'x': 485, 'y': 195}, {'x': 502, 'y': 195}, # D
            {'x': 515, 'y': 195}, {'x': 525, 'y': 195}, # M
            {'x': 535, 'y': 195}, {'x': 550, 'y': 195}, {'x': 562, 'y': 195}, {'x': 575, 'y': 195} # Y
        ],
        'fecha_nacimiento2': [
             {'x': 145, 'y': 360, 'page': 1}, {'x': 155, 'y': 360, 'page': 1}, # D
             {'x': 165, 'y': 360, 'page': 1}, {'x': 180, 'y': 360, 'page': 1}, # M
             {'x': 195, 'y': 360, 'page': 1}, {'x': 208, 'y': 360, 'page': 1}, {'x': 218, 'y': 360, 'page': 1}, {'x': 232, 'y': 360, 'page': 1} # Y
        ],
        'sexo': {
            '0': {'x': 341, 'y': 171, 'fontsize': 4},  # Masculino
            '1': {'x': 297, 'y': 171, 'fontsize': 4},  # Femenino
        },
        'sexo_identificacion': {
            '0': {'x': 383, 'y': 171, 'fontsize': 4},  # Masculino
            '1': {'x': 363, 'y': 171, 'fontsize': 4},  # Femenino
        },
        # Bloque 1: Datos del trámite (5 X's fijas)
        'datos_tramite': [
            {'x': 175, 'y': 88},   # Tipo de trámite
            {'x': 328, 'y': 78},  # Tipo de afiliación
            {'x': 505, 'y': 78},  # Régimen
            {'x': 575, 'y': 89},  # contribucion
            {'x': 148, 'y': 100},  # Tipo de afiliado
            {'x': 305, 'y': 110, 'fontsize': 4},  # Tipo de cotizante
            # {'x': 491, 'y': 348, 'fontsize': 4},  # zona
            {'x': 290, 'y': 686, 'page': 2}, # TODO: Ajustar coordenadas para la X fija en pag 3
        ],
        # Bloque 2: Administradora anterior (SURA)
        'administradora_anterior': {
            'valor': 'SURA',
            'x': 60, 'y': 256
        },
        # Bloque 3: Datos del empleador (8 campos)
        'datos_empleador': {
            'campo_variable': {'x': 60, 'y': 130, 'page': 1},  # Columna F (Empresa/Area)
            'nit': {'valor': 'NIT', 'x': 260, 'y': 130, 'page': 1},
            'numero_documento': {'valor': '123456789-55', 'x': 345, 'y': 130, 'page': 1},
            'direccion': {'valor': 'calle 15 #26-101', 'x': 70, 'y': 155, 'page': 1},
            'telefono': {'valor': '3164219523', 'x': 519, 'y': 155, 'page': 1},
            'correo': {'valor': 'contratacionrh@vallesolidario.com', 'x': 80, 'y': 175, 'fontsize': 10, 'page': 1},
            'ciudad': {'valor': 'YUMBO', 'x': 480, 'y': 176, 'page': 1},
            'departamento': {'valor': 'VALLE DEL CAUCA', 'x': 315, 'y': 175, 'fontsize': 9, 'page': 1},
            'pais': {'valor': 'COLOMBIA', 'x': 515, 'y': 175, 'fontsize': 8, 'page': 0},
            'tipo_documento': {'valor': 'CC', 'x': 55, 'y': 175, 'fontsize': 8, 'page': 0},
        }
    },
    'EMSSANAR': {
        'archivo': 'Formulario_Único_de_Afiliaciones_y_Registro_Novedades_EPS_EMSSANAR.pdf',
        'campos': {
            'CEDULA': {'x': 195, 'y': 171.5},
            'PRIMER_APELLIDO': {'x': 75, 'y': 153},
            'SEGUNDO_APELLIDO': {'x': 215, 'y': 153},
            'PRIMER_NOMBRE': {'x': 350, 'y': 153},
            'SEGUNDO_NOMBRE': {'x': 490, 'y': 153},
            'PAIS_NACIMIENTO': {'x': 210, 'y': 190, 'fontsize': 7},
            'DEPARTAMENTO_NACIMIENTO': {'x': 305, 'y': 190, 'fontsize': 4},
            'CIUDAD_NACIMIENTO': {'x': 377, 'y': 190, 'fontsize': 7},
            # Nuevos campos solicitados (Coordenadas pendientes de definir por el usuario)
            'AFP': {'x': 195, 'y': 259, 'fontsize': 8}, 
            'SALARIO_BASICO': {'x': 331, 'y': 259, 'fontsize': 8}, 
            'CORREO_ELECTRONICO': {'x': 430, 'y': 280, 'fontsize': 6},
            'DIRECCION_RESIDENCIA': {'x': 60, 'y': 280, 'fontsize': 8}, 
            'TELEFONO_MOVIL': {'x': 345, 'y': 280, 'fontsize': 8}, 
            'BARRIO': {'x': 277, 'y': 305, 'fontsize': 6}, 
            'CIUDAD_RESIDENCIA': {'x': 190, 'y': 305, 'fontsize': 8}, 
            'DEPARTAMENTO_NACIMIENTO2': {'x': 40, 'y': 305, 'fontsize': 8, 'page': 0}, # Pagina 1
        },
        'fecha_nacimiento': [
            {'x': 457, 'y': 190}, {'x': 473, 'y': 190}, # D
            {'x': 485, 'y': 190}, {'x': 498, 'y': 190}, # M
            {'x': 510, 'y': 190}, {'x': 519, 'y': 190}, {'x': 529, 'y': 190}, {'x': 536, 'y': 190} # Y
        ],
        'fecha_nacimiento2': [
             {'x': 125, 'y': 240, 'page': 1}, {'x': 138, 'y': 240, 'page': 1}, # D
             {'x': 151, 'y': 240, 'page': 1}, {'x': 165, 'y': 240, 'page': 1}, # M
             {'x': 178, 'y': 240, 'page': 1}, {'x': 190, 'y': 240, 'page': 1}, {'x': 202, 'y': 240, 'page': 1}, {'x': 214, 'y': 240, 'page': 1} # Y
        ],
        'sexo': {
            '0': {'x': 334, 'y': 170, 'fontsize': 4},  # Masculino
            '1': {'x': 298, 'y': 170, 'fontsize': 4},  # Femenino
        },
        'sexo_identificacion': {
            '0': {'x': 412, 'y': 170, 'fontsize': 4},  # Masculino
            '1': {'x': 374, 'y': 170, 'fontsize': 4},  # Femenino
        },
        # Bloque 1: Datos del trámite (5 X's fijas)
        'datos_tramite': [
            {'x': 140, 'y': 100},   # Tipo de trámite
            {'x': 299, 'y': 93},  # Tipo de afiliación
            {'x': 460, 'y': 97},  # Régimen
            {'x': 581, 'y': 102},  # contribucion
            {'x': 52, 'y': 121},  # Tipo de afiliado
            {'x': 292, 'y': 120, 'fontsize': 4},  # Tipo de cotizante
            {'x': 491, 'y': 298, 'fontsize': 4},  # zona
        ],
        # Bloque 2: Administradora anterior (SURA)
        'administradora_anterior': {
            'valor': 'SURA',
            'x': 60, 'y': 259
        },
        # Bloque 3: Datos del empleador (8 campos)
        'datos_empleador': {
            'campo_variable': {'x': 90, 'y': 749},  # Columna F (Empresa/Area)
            'nit': {'valor': 'NIT', 'x': 288, 'y': 751},
            'numero_documento': {'valor': '123456789-55', 'x': 315, 'y': 749},
            'direccion': {'valor': 'calle 15 #26-101', 'x': 90, 'y': 767},
            'telefono': {'valor': '3164219523', 'x': 218, 'y': 767},
            'correo': {'valor': 'contratacionrh@vallesolidario.com', 'x': 299, 'y': 764, 'fontsize': 4},
            'ciudad': {'valor': 'YUMBO', 'x': 457, 'y': 767},
            'departamento': {'valor': 'VALLE DEL CAUCA', 'x': 380, 'y': 767, 'fontsize': 7},
            'pais': {'valor': 'COLOMBIA', 'x': 90, 'y': 189, 'fontsize': 8},
            'tipo_documento': {'valor': 'CC', 'x': 75, 'y': 171.5, 'fontsize': 8},
        },
        'anexos': [
            {
                'archivo': 'Carta_Derechos_Deberes_EPS_EMSSANAR.pdf',
                'campos': {
                    'CIUDAD_NACIMIENTO': {'x': 160, 'y': 475, 'fontsize': 10},       # Municipio
                    'DEPARTAMENTO_NACIMIENTO': {'x': 360, 'y': 475, 'fontsize': 10}, # Departamento
                },
                'fecha_ingreso_3_partes': [ # Dia, Mes, Año (2 ultimos digitos)
                    {'x': 205, 'y': 450}, # DD
                    {'x': 254, 'y': 450}, # MM
                    {'x': 310, 'y': 450}, # YY
                ],
                'marcas_fijas': [
                    {'x': 88, 'y': 215}, # Primera X fija
                    {'x': 88, 'y': 270}, # Segunda X fija
                    {'x': 88, 'y': 320}, # Tercera X fija
                    {'x': 88, 'y': 370}, # Cuarta X fija    
                    {'x': 88, 'y': 370}, # Quinta X fija
                    {'x': 88, 'y': 420}, # Sexta X fija
                ]
            }
        ]
    },
    'SALUD TOTAL': {
        'archivo': 'FORMULARIO-DE-AFILIACION-UNICO-Y-REGISTRO-DE-NOVEDADES_SALUDTOTAL.pdf',
        'campos': {
            'CEDULA': {'x': 215, 'y': 275},
            'PRIMER_APELLIDO': {'x': 75, 'y': 250},
            'SEGUNDO_APELLIDO': {'x': 215, 'y': 250},
            'PRIMER_NOMBRE': {'x': 360, 'y': 250},
            'SEGUNDO_NOMBRE': {'x': 500, 'y': 250}, 

            'AFP': {'x': 248, 'y': 330, 'fontsize': 8}, 
            'SALARIO_BASICO': {'x': 441, 'y': 330, 'fontsize': 8}, 
            'CORREO_ELECTRONICO': {'x': 498, 'y': 355, 'fontsize': 6},
            'DIRECCION_RESIDENCIA': {'x': 80, 'y': 355, 'fontsize': 8}, 
            'TELEFONO_MOVIL': {'x': 385, 'y': 355, 'fontsize': 8}, 
            'BARRIO': {'x': 358, 'y': 375, 'fontsize': 6}, 
            'CIUDAD_RESIDENCIA': {'x': 120, 'y': 375, 'fontsize': 8}, 
            'DEPARTAMENTO_NACIMIENTO2': {'x': 500, 'y': 375, 'fontsize': 8, 'page': 0},
            'CEDULA_PAGINA_3': {'x': 268, 'y': 736, 'fontsize': 10, 'page': 2}, # TODO: Ajustar coordenadas
        },
        'fecha_nacimiento': [
            {'x': 492, 'y': 275}, {'x': 512, 'y': 275}, # D
            {'x': 526, 'y': 275}, {'x': 544, 'y': 275}, # M
            {'x': 564, 'y': 275}, {'x': 578, 'y': 275}, {'x': 595, 'y': 275}, {'x': 615, 'y': 275} # Y
        ],
        'fecha_nacimiento2': [
             {'x': 514, 'y': 365, 'page': 1}, {'x': 524, 'y': 365, 'page': 1}, # D
             {'x': 541, 'y': 365, 'page': 1}, {'x': 554, 'y': 365, 'page': 1}, # M
             {'x': 569, 'y': 365, 'page': 1}, {'x': 588, 'y': 365, 'page': 1}, {'x': 603, 'y': 365, 'page': 1}, {'x': 620, 'y': 365, 'page': 1} # Y
        ],        
        'sexo': {
            '0': {'x': 474, 'y': 274, 'fontsize': 4},  # Masculino
            '1': {'x': 412, 'y': 274, 'fontsize': 4},  # Femenino
        },
        
        # Bloque 1: Datos del trámite (5 X's fijas)
        'datos_tramite': [
            {'x': 222, 'y': 189},   # Tipo de trámite
            {'x': 464, 'y': 169},  # Tipo de afiliación
            {'x': 547, 'y': 188},  # Régimen
            
            {'x': 138, 'y': 208},  # Tipo de afiliado
            {'x': 380, 'y': 208, 'fontsize': 4},  # Tipo de cotizante
            # {'x': 491, 'y': 348, 'fontsize': 4},  # zona
            
        ],
        # Bloque 2: Administradora anterior (SURA)
        'administradora_anterior': {
            'valor': 'SURA',
            'x': 78, 'y': 330
        },
        # Bloque 3: Datos del empleador (8 campos)
        'datos_empleador': {
            'campo_variable': {'x': 66, 'y': 835},  # Columna F (Empresa/Area)
            'nit': {'valor': 'NIT', 'x': 309, 'y': 837, 'fontsize': 6},
            'numero_documento': {'valor': '123456789-55', 'x': 345, 'y': 835},
            'direccion': {'valor': 'calle 15 #26-101', 'x': 66, 'y': 855},
            'telefono': {'valor': '3164219523', 'x': 249, 'y': 855},
            'correo': {'valor': 'contratacionrh@vallesolidario.com', 'x': 312, 'y': 853, 'fontsize': 6},
            'ciudad': {'valor': 'YUMBO', 'x': 428, 'y': 855},
            'departamento': {'valor': 'VALLE DEL CAUCA', 'x': 533, 'y': 853, 'fontsize': 6},
           
            'tipo_documento': {'valor': 'CC', 'x': 175, 'y': 275, 'fontsize': 6},
        }
    },
    'ASMET SALUD': None,
    'NUEVA EPS': None,
    'ASOCIACION MUTUAL SER EMPRESA SOLIDARIA DE SALUD EPS-S': None,
    'FAMISANAR': None,
    'COOSALUD': {
        'archivo': 'Formulario_de_Afiliacion_y_Registro_de_Novedades_eps_coosalud.pdf',
        'campos': {
            'CEDULA': {'x': 215, 'y': 190},
            'PRIMER_APELLIDO': {'x': 75, 'y': 170},
            'SEGUNDO_APELLIDO': {'x': 215, 'y': 170},
            'PRIMER_NOMBRE': {'x': 350, 'y': 170},
            'SEGUNDO_NOMBRE': {'x': 470, 'y': 170},
            
            
            
            
            'AFP': {'x': 245, 'y': 250, 'fontsize': 8}, 
            'SALARIO_BASICO': {'x': 441, 'y': 250, 'fontsize': 8}, 
            'CORREO_ELECTRONICO': {'x': 425, 'y': 265, 'fontsize': 5},
            'DIRECCION_RESIDENCIA': {'x': 64, 'y': 265, 'fontsize': 8}, 
            'TELEFONO_MOVIL': {'x': 365, 'y': 265, 'fontsize': 8}, 
            'BARRIO': {'x': 310, 'y': 290, 'fontsize': 5}, 
            'CIUDAD_RESIDENCIA': {'x': 120, 'y': 290, 'fontsize': 8}, 
            'DEPARTAMENTO_NACIMIENTO2': {'x': 460, 'y': 290, 'fontsize': 8, 'page': 0},
            'CEDULA_PAGINA_3': {'x': 268, 'y': 736, 'fontsize': 10, 'page': 2}, # TODO: Ajustar coordenadas
        },
        'fecha_nacimiento': [
            {'x': 452, 'y': 192}, {'x': 464, 'y': 192}, # D
            {'x': 472, 'y': 192}, {'x': 484, 'y': 192}, # M
            {'x': 492, 'y': 192}, {'x': 503, 'y': 192}, {'x': 514, 'y': 192}, {'x': 524, 'y': 192} # Y
        ],
        'fecha_nacimiento2': [
             {'x': 470, 'y': 240, 'page': 1}, {'x': 478, 'y': 240, 'page': 1}, # D
             {'x': 488, 'y': 240, 'page': 1}, {'x': 497, 'y': 240, 'page': 1}, # M
             {'x': 504, 'y': 240, 'page': 1}, {'x': 516, 'y': 240, 'page': 1}, {'x': 524, 'y': 240, 'page': 1}, {'x': 533, 'y': 240, 'page': 1} # Y
        ],        
        'sexo': {
            '0': {'x': 405, 'y': 190, 'fontsize': 4},  # Masculino
            '1': {'x': 366, 'y': 190, 'fontsize': 4},  # Femenino
        },
        
        # Bloque 1: Datos del trámite (5 X's fijas)
        'datos_tramite': [
            {'x': 180, 'y': 107},   # Tipo de trámite
            {'x': 434, 'y': 90},  # Tipo de afiliación
            {'x': 536, 'y': 98},  # Régimen
            
            {'x': 124, 'y': 126},  # Tipo de afiliado
            {'x': 323, 'y': 126, 'fontsize': 4},  # Tipo de cotizante
            # {'x': 491, 'y': 348, 'fontsize': 4},  # zona
            
        ],
        # Bloque 2: Administradora anterior (SURA)
        'administradora_anterior': {
            'valor': 'SURA',
            'x': 78, 'y': 250
        },
        # Bloque 3: Datos del empleador (8 campos)
        'datos_empleador': {
            'campo_variable': {'x': 66, 'y': 745},  # Columna F (Empresa/Area)
            'nit': {'valor': 'NIT', 'x': 277, 'y': 745},
            'numero_documento': {'valor': '123456789-55', 'x': 315, 'y': 745},
            'direccion': {'valor': 'calle 15 #26-101', 'x': 66, 'y': 765},
            'telefono': {'valor': '3164219523', 'x': 224, 'y': 765},
            'correo': {'valor': 'contratacionrh@vallesolidario.com', 'x': 294, 'y': 761, 'fontsize': 5},
            'ciudad': {'valor': 'YUMBO', 'x': 400, 'y': 765},
            'departamento': {'valor': 'VALLE DEL CAUCA', 'x': 483, 'y': 765, 'fontsize': 6},
           
            'tipo_documento': {'valor': 'CC', 'x': 165, 'y': 190, 'fontsize': 8},
        }
    },
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

        # -- FUNCIONES AUXILIARES PARA MANEJO DE PÁGINAS --
        def get_page(page_num=0):
            """Obtiene la página segura, o None si no existe."""
            if page_num < len(doc):
                return doc[page_num]
            return None

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
        mapa_fecha2 = config.get('fecha_nacimiento2', [])
        mapa_sexo = config.get('sexo', {})
        mapa_sexo_2 = config.get('sexo_2', {}) # Nuevo mapa para sexo duplicado
        mapa_sexo_identificacion = config.get('sexo_identificacion', {})

        # -- INSERCIÓN DE DATOS GENÉRICOS --
        
        # Mapeo de variables locales a claves en la configuración
        campos_simples = {
            'CEDULA': cedula,
            'CEDULA_PAGINA_3': cedula, # Campo duplicado para pagina 3
            'PRIMER_APELLIDO': primer_apellido,
            'SEGUNDO_APELLIDO': segundo_apellido,
            'PRIMER_NOMBRE': primer_nombre,
            'SEGUNDO_NOMBRE': segundo_nombre,
            'PAIS_NACIMIENTO': pais_nacimiento,
            'DEPARTAMENTO_NACIMIENTO': departamento_nacimiento,
            'DEPARTAMENTO_NACIMIENTO2': departamento_nacimiento, # Mismo valor, diferente campo
            'CIUDAD_NACIMIENTO': ciudad_nacimiento,
            'PAIS_NACIMIENTO_2': pais_nacimiento, # Duplicado
            'TIPO_DOCUMENTO_CC': 'CC', # Constante
            # Nuevos campos agregados
            'AFP': datos_empleado.get('AFP', ''),
            'SALARIO_BASICO': datos_empleado.get('SALARIO_BASICO', ''),
            'CORREO_ELECTRONICO': datos_empleado.get('CORREO_ELECTRONICO', ''),
            'DIRECCION_RESIDENCIA': datos_empleado.get('DIRECCION_RESIDENCIA', ''),
            'TELEFONO_MOVIL': datos_empleado.get('TELEFONO_MOVIL', ''),
            'BARRIO': datos_empleado.get('BARRIO', ''),
            'CIUDAD_RESIDENCIA': datos_empleado.get('CIUDAD_RESIDENCIA', ''),
            'CIUDAD_RESIDENCIA_3': datos_empleado.get('CIUDAD_RESIDENCIA', ''),
        }

        for clave_campo, valor in campos_simples.items():
            if valor and clave_campo in mapa_campos:
                coords = mapa_campos[clave_campo]

                # Determinar página (default 0)
                page_idx = coords.get('page', 0)
                page = get_page(page_idx)

                if page:
                    # Priorizar fontsize de la configuración, sino usar lógica por defecto
                    if 'fontsize' in coords:
                        size = coords['fontsize']
                    else:
                        # Ajustar tamaño de fuente por defecto para ciertos campos
                        size = 8 if 'DEPARTAMENTO' in clave_campo else 10

                    # Manejo especial para TELEFONO_MOVIL con guión (excepto para SANITAS)
                    if clave_campo == 'TELEFONO_MOVIL' and '-' in str(valor) and nombre_eps != 'SANITAS':
                        # Dividir por el guión
                        telefonos = str(valor).split('-')
                        # Insertar primer teléfono en la posición original
                        insertar_texto_en_pdf(page, telefonos[0].strip(), coords['x'], coords['y'], fontsize=size)
                        # Insertar segundo teléfono 10 puntos más abajo
                        if len(telefonos) > 1:
                            insertar_texto_en_pdf(page, telefonos[1].strip(), coords['x'], coords['y'] + 10, fontsize=size)
                    else:
                        insertar_texto_en_pdf(page, valor, coords['x'], coords['y'], fontsize=size)

        # -- INSERCIONES ESPECIALES --

        # Insertar FECHA DE NACIMIENTO
        if fecha_nacimiento and mapa_fecha:
            # Asumimos que fecha_nacimiento principal está en página 0 por defecto si no se especifica
            # Pero sería mejor que la función auxiliar maneje la página también si se pasa en coords
             # Validar que tengamos coordenadas para los 8 dígitos
            if len(mapa_fecha) >= 8:
                 fecha_ddmmyyyy = convertir_fecha_yyyymmdd_a_ddmmyyyy(fecha_nacimiento)
                 if fecha_ddmmyyyy and len(fecha_ddmmyyyy) == 8:
                    for i, digito in enumerate(fecha_ddmmyyyy):
                        coords = mapa_fecha[i]
                        page_idx = coords.get('page', 0)
                        page = get_page(page_idx)
                        if page:
                             insertar_texto_en_pdf(page, digito, coords['x'], coords['y'], fontsize=10)


        # Insertar FECHA DE NACIMIENTO 2 (si existe)
        if fecha_nacimiento and mapa_fecha2:
             if len(mapa_fecha2) >= 8:
                 # Usar FECHA_INGRESO para fecha_nacimiento2
                 fecha_ingreso = datos_empleado.get('FECHA_INGRESO', '')
                 fecha_ddmmyyyy = convertir_fecha_yyyymmdd_a_ddmmyyyy(fecha_ingreso)
                 if fecha_ddmmyyyy and len(fecha_ddmmyyyy) == 8:
                    for i, digito in enumerate(fecha_ddmmyyyy):
                        coords = mapa_fecha2[i]
                        page_idx = coords.get('page', 0) # Aquí debe venir 'page': 1
                        page = get_page(page_idx)
                        if page:
                             insertar_texto_en_pdf(page, digito, coords['x'], coords['y'], fontsize=10)

        # Marcar SEXO
        if codigo_sexo and str(codigo_sexo) in mapa_sexo:
            coords = mapa_sexo[str(codigo_sexo)]
            page_idx = coords.get('page', 0)
            page = get_page(page_idx)
            if page:
                marcar_x_en_pdf(page, coords['x'], coords['y'], size=7)

        # Marcar SEXO 2 (duplicado)
        if codigo_sexo and str(codigo_sexo) in mapa_sexo_2:
            coords = mapa_sexo_2[str(codigo_sexo)]
            page_idx = coords.get('page', 0)
            page = get_page(page_idx)
            if page:
                marcar_x_en_pdf(page, coords['x'], coords['y'], size=7)

        # Marcar SEXO IDENTIFICACION
        if codigo_sexo and str(codigo_sexo) in mapa_sexo_identificacion:
            coords = mapa_sexo_identificacion[str(codigo_sexo)]
            page_idx = coords.get('page', 0)
            page = get_page(page_idx)
            if page:
                marcar_x_en_pdf(page, coords['x'], coords['y'], size=7)

        # -- NUEVOS BLOQUES --

        # 1. Datos del trámite (X's fijas)
        datos_tramite = config.get('datos_tramite', [])
        for coords in datos_tramite:
            page_idx = coords.get('page', 0)
            page = get_page(page_idx)
            if page:
                marcar_x_en_pdf(page, coords['x'], coords['y'], size=7)

        # 2. Administradora anterior
        admin_anterior = config.get('administradora_anterior')
        if admin_anterior:
            page_idx = admin_anterior.get('page', 0)
            page = get_page(page_idx)
            if page:
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
                elif key == 'numero_documento':
                    # Asignar NIT dinámicamente según la empresa
                    empresa_key = valor_empresa.strip()
                    if empresa_key in NITS_EMPRESAS:
                        valor = NITS_EMPRESAS[empresa_key]
                    else:
                        valor = info.get('valor', '')
                elif 'valor' in info:
                    valor = info['valor']
                
                if valor:
                    page_idx = info.get('page', 0)
                    page = get_page(page_idx)
                    if page:
                        print(f"DEBUG: Insertando campo '{key}' -> Valor: '{valor}' en ({info['x']}, {info['y']}) Pagina: {page_idx}")
                        text_fontsize = info.get('fontsize', 10) # Obtener fontsize de la configuración, default 10
                        insertar_texto_en_pdf(page, valor, info['x'], info['y'], fontsize=text_fontsize)


        # Guardar el PDF generado
        doc.save(output_path)
        doc.close()

        # Procesar Anexos (si existen)
        anexos_config = config.get('anexos', [])
        if anexos_config:
            # Reabrir el documento principal para añadir páginas
            # Nota: fitz no permite editar el mismo archivo abierto, 
            # así que trabajamos con archivos temporales o reabrimos
            doc_main = fitz.open(output_path)
            
            for anexo in anexos_config:
                archivo_anexo = anexo.get('archivo')
                if not archivo_anexo:
                    continue
                
                path_anexo_template = os.path.join(BASE_DIR, 'formatos', archivo_anexo)
                if not os.path.exists(path_anexo_template):
                    print(f"Advertencia: No se encontró el anexo {path_anexo_template}")
                    continue
                
                try:
                    doc_anexo = fitz.open(path_anexo_template)
                    page_anexo = doc_anexo[0] # Asumimos 1 pagina por anexo por ahora, o iteramos si son varias
                    
                    # 1. Campos simples del anexo
                    campos_anexo = anexo.get('campos', {})
                    for clave_campo, info in campos_anexo.items():
                        valor = campos_simples.get(clave_campo, '')
                        if valor:
                            insertar_texto_en_pdf(page_anexo, valor, info['x'], info['y'], fontsize=info.get('fontsize', 10))
                    
                    # 2. Fecha Ingreso 3 partes (DD, MM, YY)
                    fecha_ingreso_3_partes = anexo.get('fecha_ingreso_3_partes', [])
                    fecha_ingreso_raw = datos_empleado.get('FECHA_INGRESO', '') # YYYYMMDD
                    if fecha_ingreso_3_partes and fecha_ingreso_raw and len(fecha_ingreso_raw) == 8:
                        # Extraer partes
                        yyyy = fecha_ingreso_raw[0:4]
                        mm = fecha_ingreso_raw[4:6]
                        dd = fecha_ingreso_raw[6:8]
                        yy = yyyy[2:4] # Ultimos 2 digitos
                        
                        partes = [dd, mm, yy]
                        
                        if len(fecha_ingreso_3_partes) >= 3:
                            for i, parte in enumerate(partes):
                                coords = fecha_ingreso_3_partes[i]
                                insertar_texto_en_pdf(page_anexo, parte, coords['x'], coords['y'], fontsize=10)

                    # 3. Marcas Fijas
                    marcas_fijas = anexo.get('marcas_fijas', [])
                    for marca in marcas_fijas:
                        marcar_x_en_pdf(page_anexo, marca['x'], marca['y'], size=7)

                    # Unir al documento principal
                    doc_main.insert_pdf(doc_anexo)
                    doc_anexo.close()

                except Exception as e:
                    print(f"Error procesando anexo {archivo_anexo}: {e}")
            
            # Guardar cambios finales con anexos
            doc_main.saveIncr() # Guardado incremental sobre el mismo archivo
            doc_main.close()

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