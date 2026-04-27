# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Descripción del Proyecto

Sistema web Django para la generación automática de formularios de afiliación a EPS (Entidades Promotoras de Salud) para la Corporación Hacia un Valle Solidario (CHVS). El sistema busca empleados en Google Sheets y genera PDFs pre-llenados con sus datos en los formatos oficiales de cada EPS.

## Comandos Esenciales

### Desarrollo Local

```bash
# Activar entorno virtual
# Windows: .\venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Navegar al directorio de Django
cd formularios

# Iniciar servidor de desarrollo
python manage.py runserver

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recolectar archivos estáticos
python manage.py collectstatic --noinput
```

### Instalación de Dependencias

```bash
# Desarrollo local (sin PostgreSQL - recomendado para Windows)
pip install -r requirements-dev.txt

# Producción (incluye psycopg2-binary para PostgreSQL)
pip install -r requirements.txt
```

### Gestión de Base de Datos

```bash
# Crear migraciones después de cambios en models.py
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Abrir shell interactivo de Django
python manage.py shell
```

### Scripts de Utilidad

```bash
# Desde el directorio raíz (formularios_eps/)
python test/test_google_sheets.py         # Probar conexión con Google Sheets
python test/test_pdf_generation.py        # Probar generación de PDFs
python test/buscar_columnas.py            # Buscar columnas en Google Sheets
python test/list_users.py                 # Listar usuarios de la BD
```

## Arquitectura del Proyecto

### Estructura de Directorios

```
formularios_eps/
├── formularios/                    # Proyecto Django principal
│   ├── formatos_eps/              # App Django - lógica principal
│   │   ├── views.py               # Vistas: login, búsqueda, generación PDF
│   │   ├── google_sheets.py       # Integración con Google Sheets API
│   │   ├── pdf_generator.py       # Motor de generación de PDFs (PyMuPDF)
│   │   ├── urls.py                # URLs de la aplicación
│   │   ├── models.py              # Modelos (actualmente usa solo Django Auth)
│   │   └── templates/             # Plantillas HTML
│   ├── formularios/               # Configuración Django
│   │   ├── settings.py            # Configuración principal
│   │   └── urls.py                # URLs raíz
│   ├── static/                    # Archivos estáticos (CSS, JS)
│   ├── templates/                 # Plantillas HTML base
│   ├── manage.py                  # CLI de Django
│   ├── db.sqlite3                 # Base de datos SQLite (desarrollo)
│   └── service_account.json       # Credenciales Google (NO commitear)
├── formatos/                      # Plantillas PDF de formularios EPS
├── test/                          # Scripts de prueba y utilidades
├── archivosmd/                    # Documentación adicional
├── .env                           # Variables de entorno (NO commitear)
├── requirements.txt               # Dependencias producción
├── requirements-dev.txt           # Dependencias desarrollo
└── railway.json                   # Configuración Railway
```

### Flujo de Datos Principal

1. **Autenticación**: Usuario inicia sesión (Django Auth)
2. **Búsqueda**: Usuario ingresa cédula → `views.search_results_view()`
3. **Google Sheets**: `google_sheets.find_row_by_cedula()` busca en hojas "Planta" y "Manipuladoras"
4. **Generación PDF**: `views.generar_pdf_view()` → `pdf_generator.rellenar_pdf_empleado()`
5. **Descarga**: PDF generado se retorna como FileResponse

### Componentes Clave

#### 1. Google Sheets Integration (`google_sheets.py`)

- **Spreadsheet ID**: `1KAtsyGy1-vyPFrdux3WWeGagL8F4zHCRMZqBKew0WYw`
- **Hojas consultadas**:
  - `Planta` - Empleados de planta
  - `Manipuladoras` - Manipuladoras de alimentos
  - `Codigo Pais-Dpto-Ciudad` - Datos geográficos
- **Autenticación**:
  - Producción: Variable `GOOGLE_CREDENTIALS` (JSON string)
  - Desarrollo: Archivo `formularios/service_account.json`
- **Funciones importantes**:
  - `find_row_by_cedula(cedula)`: Busca empleado, retorna registro más reciente si hay duplicados
  - `buscar_departamento_por_ciudad(ciudad)`: Busca departamento por nombre de ciudad
  - `get_sheet_data(sheet_name)`: Obtiene todos los datos de una hoja como lista de diccionarios

**Manejo de duplicados**: La función `get_sheet_data()` agrega sufijos (`_1`, `_2`) a columnas con nombres duplicados.

#### 2. PDF Generator (`pdf_generator.py`)

Motor de generación de PDFs usando PyMuPDF (fitz). Arquitectura basada en configuración.

**Estructura de configuración por EPS** (`CONFIGURACION_FORMATOS`):

```python
{
    'EPS_NOMBRE': {
        'archivo': 'nombre_plantilla.pdf',
        'campos': {                         # Campos de texto
            'CEDULA': {'x': 130, 'y': 181},
            'PRIMER_APELLIDO': {'x': 75, 'y': 163, 'fontsize': 10}
        },
        'fecha_nacimiento': [               # Coordenadas para 8 dígitos DDMMYYYY
            {'x': 290, 'y': 200}, ...
        ],
        'fecha_nacimiento2': [              # Segunda fecha (FECHA_INGRESO) en otra página
            {'x': 487, 'y': 728, 'page': 1}, ...
        ],
        'fecha_nacimiento3': [              # Tercera fecha (FECHA_INGRESO) en una página adicional
            {'x': 178, 'y': 415, 'page': 2}, ...  # Solo ASMET SALUD por ahora
        ],
        'sexo': {                           # Marcas X según código
            '0': {'x': 302.5, 'y': 176.5},  # Masculino
            '1': {'x': 267.5, 'y': 176.5}   # Femenino
        },
        'datos_tramite': [                  # X's fijas
            {'x': 121, 'y': 120}, ...
        ],
        'datos_empleador': {                # Datos de la empresa
            'campo_variable': {'x': 90, 'y': 588},
            'nit': {'valor': 'NIT', 'x': 235, 'y': 588}
        },
        'anexos': [                         # PDFs adicionales (ej: EMSSANAR)
            {
                'archivo': 'anexo.pdf',
                'campos': {...},
                'marcas_fijas': [...]
            }
        ]
    }
}
```

**NITs de Empresas** (`NITS_EMPRESAS`): Mapeo de nombre de empresa a NIT. Se usa en `datos_empleador.numero_documento`.

**Funciones principales**:
- `rellenar_pdf_empleado(datos_empleado, output_path)`: Función principal de generación
- `insertar_texto_en_pdf(page, texto, x, y, fontsize)`: Inserta texto en coordenadas
- `marcar_x_en_pdf(page, x, y, size)`: Dibuja marca X
- `convertir_fecha_yyyymmdd_a_ddmmyyyy(fecha_str)`: Convierte formato de fecha
- `split_nombres(nombres_completos)`: Divide nombres en primer y segundo nombre

**EPSs Configuradas** (con plantilla PDF):
- COMFENALCO VALLE ✅ (completo con anexos)
- SOS ✅
- SANITAS ✅
- EMSSANAR ✅ (incluye anexo "Carta_Derechos_Deberes_EPS_EMSSANAR.pdf")
- SALUD TOTAL ✅
- COOSALUD ✅
- ASMET SALUD ✅ (3 páginas: formulario principal + Reporte de Novedades + Carta de Deberes y Derechos)

**EPSs sin configurar**: Retornan `None`, generan `ValueError` al intentar generar PDF.

#### 3. Views (`views.py`)

Todas las vistas excepto login/logout requieren el permiso `formatos_eps.ver_eps`.

- `login_view` / `logout_view`: Autenticación Django Auth
- `dashboard_view`: Panel con accesos por módulo
- `search_view`: Formulario de búsqueda por cédula (muestra solo EPS con plantilla PDF presente en `formatos/`)
- `search_results_view`: Muestra datos del empleado encontrado
- `generar_pdf_view`: Genera y descarga PDF individual (FileResponse)
- `generar_pdf_masivo_view`: Recibe lista de cédulas (POST), genera ZIP con PDFs + `errores.txt`
- `generar_pdf_masivo_filtro_view`: Genera ZIP con PDFs filtrando toda la BD (EPS, empresa, área, fecha ingreso, solo activos, etc.)

**Funciones privadas de apoyo** (prefijo `_`):
- `_normalizar_resultado_busqueda(result_data)`: Mapeo de columnas Sheets → diccionario para la vista de resultados
- `_normalizar_datos_para_pdf(datos_empleado)`: Mapeo más completo para la generación PDF (incluye AFP, salario, dirección, etc.)
- `_parsear_cedulas(raw_value)`: Extrae cédulas numéricas de texto libre (separadas por cualquier carácter no numérico)
- `_es_activo(row)`: Regla flexible de estado activo — verifica `FECHA RETIRO`, luego `ESTADO`, luego `ACTIVO`
- `_obtener_registros_unificados()`: Combina Planta + Manipuladoras desduplicando por cédula más reciente
- `_filtrar_registros(rows, filtros)`: Aplica filtros sobre registros combinados

**Campo especial `_origen_hoja`**: Indica si el empleado viene de "Planta" o "Manipuladoras". Se usa en `pdf_generator.py` para determinar qué campo usar en `datos_empleador.campo_variable`:
- Planta → `EMPRESA`
- Manipuladoras → `PROGRAMA AL QUE PERTENECE`

**Mappings de columnas Google Sheets con nombres no obvios**:
- `CORREO_ELECTRONICO` ← columna `CORREOS`
- `TELEFONO_MOVIL` ← columna `NUMERO TELEFONICO ` (con espacio al final — usar `.strip()`)
- `CIUDAD_RESIDENCIA` ← columna `CIUDAD` con fallback a `MUNICIPIO`
- `FECHA_INGRESO` ← columna `FECHA DE INGRESO (AAAAMMDD)`

#### 4. Permisos y Grupos (`models.py`)

`AccesoModulos` es un modelo virtual (sin tabla) que define permisos personalizados:
- `ver_eps`: Acceso al módulo de formularios EPS
- `ver_certificados`: Acceso a certificados laborales
- `ver_incapacidades`: Acceso a incapacidades

Los grupos de usuarios se administran desde el admin de Django y se asocian a estos permisos. El dashboard muestra/oculta módulos según los permisos del usuario.

### Configuración de Entorno

#### Detección Automática de Entorno

El archivo `settings.py` detecta automáticamente el entorno:

```python
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Producción: PostgreSQL, DEBUG=False por defecto
    DATABASES = dj_database_url.parse(DATABASE_URL)
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'
else:
    # Desarrollo: SQLite, DEBUG=True por defecto
    DATABASES = {'default': {'ENGINE': 'sqlite3', 'NAME': 'db.sqlite3'}}
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'
```

#### Variables de Entorno Importantes

| Variable | Desarrollo | Producción | Descripción |
|----------|-----------|-----------|-------------|
| `DATABASE_URL` | No definir | Auto (Railway) | Trigger de modo producción |
| `GOOGLE_CREDENTIALS` | Opcional (usar archivo) | Requerido (JSON) | Credenciales Google Sheets |
| `SECRET_KEY` | Auto-generado | Requerido | Clave secreta Django |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Dominio Railway | Hosts permitidos |
| `CSRF_TRUSTED_ORIGINS` | No requerido | Requerido | URLs CSRF trusted |
| `DEBUG` | `True` (auto) | `False` (auto) | Modo debug |

## Patrones y Convenciones

### Agregar Nueva EPS

1. **Agregar plantilla PDF**: Colocar archivo en `formatos/`
2. **Configurar en `pdf_generator.py`**:
   ```python
   CONFIGURACION_FORMATOS['NUEVA EPS'] = {
       'archivo': 'nombre_plantilla.pdf',
       'campos': {...},
       'fecha_nacimiento': [...],
       'sexo': {...}
   }
   ```
3. **Encontrar coordenadas**: Usar `formularios/coordenadas_pdf.py` (herramienta interactiva)

### Agregar Nuevo NIT de Empresa

Editar diccionario `NITS_EMPRESAS` en `pdf_generator.py`:

```python
NITS_EMPRESAS = {
    "NUEVA EMPRESA": "901234567-8",
    ...
}
```

### Agregar Nuevos Campos de Google Sheets

1. **Agregar a `_normalizar_datos_para_pdf()` en `views.py`** (función que abastece la generación PDF):
   ```python
   'NUEVO_CAMPO': datos_empleado.get('NOMBRE EN SHEET', ''),
   ```
   Si también debe mostrarse en la vista de resultados, agregar a `_normalizar_resultado_busqueda()`.

2. **Agregar a configuración de EPS** en `pdf_generator.py`:
   ```python
   'campos': {
       'NUEVO_CAMPO': {'x': 100, 'y': 200, 'fontsize': 10}
   }
   ```

3. **Mapear en `campos_simples`** dentro de `rellenar_pdf_empleado()`:
   ```python
   campos_simples = {
       'NUEVO_CAMPO': datos_empleado.get('NUEVO_CAMPO', ''),
       ...
   }
   ```

### Manejo de Páginas en PDFs

La configuración usa `'page': N` para especificar página (0-indexed):

```python
'CAMPO': {'x': 100, 'y': 200, 'page': 1}  # Segunda página
'CAMPO': {'x': 100, 'y': 200}              # Primera página (default)
```

### Campos con Formato Especial

- **Fechas**: Se insertan dígito por dígito usando `fecha_nacimiento`, `fecha_nacimiento2` y `fecha_nacimiento3` (las dos últimas usan `FECHA_INGRESO`)
- **Sexo**: Se marca con X usando coordenadas en `sexo`, `sexo_2`, `sexo_identificacion`
- **Teléfonos con guión**: Se dividen automáticamente y se insertan en líneas separadas (10 puntos de diferencia en Y)

### Campos alias para páginas adicionales (en `campos_simples`)

Cuando un mismo dato debe aparecer en varias páginas con distintas coordenadas, se usan claves alias ya definidas en `campos_simples` dentro de `rellenar_pdf_empleado`:

| Clave alias | Valor |
|---|---|
| `CEDULA_PAGINA_3` | Cédula del empleado |
| `CEDULA_PAGINA_2_1` / `CEDULA_PAGINA_2_2` | Cédula en página 2 |
| `PAIS_NACIMIENTO_2` | País de nacimiento (duplicado) |
| `CIUDAD_NACIMIENTO_2` | Ciudad de nacimiento (duplicado) |
| `CIUDAD_RESIDENCIA_3` | Ciudad de residencia (duplicado) |
| `NOMBRE_COMPLETO_PAG3` | Apellidos + nombres en una línea (para ASMET SALUD p.3) |
| `TIPO_DOCUMENTO_PAG3` | Constante `'CC'` como texto |
| `DIRECCION_RESIDENCIA_PAG3` | Dirección de residencia (duplicado) |
| `TELEFONO_MOVIL_PAG3` | Teléfono móvil (duplicado) |

Para agregar una nueva aparición de un campo en otra página, usar una de estas claves con `'page': N` en la configuración de la EPS, o agregar un alias nuevo a `campos_simples` si no existe.

## Deploy en Railway

Railway ejecuta el comando definido en `railway.json`:

```bash
cd formularios &&
python manage.py collectstatic --noinput &&
python manage.py migrate &&
gunicorn formularios.wsgi --bind 0.0.0.0:$PORT
```

**Importante**: Las migraciones se ejecutan automáticamente en cada deploy. Para operaciones que requieren input (como `createsuperuser`), usar la terminal de Railway manualmente.

## Testing

No hay tests automatizados actualmente. Los scripts en `test/` son para verificación manual:

- `test_google_sheets.py`: Verifica conexión y lectura de datos
- `test_pdf_generation.py`: Genera PDF de prueba
- `buscar_columnas.py`: Diagnóstico de columnas en Google Sheets

## Notas Importantes

### Seguridad

- **NUNCA commitear**: `.env`, `service_account.json`, `db.sqlite3`, `*.json.key`
- `.gitignore` ya los protege, pero verificar antes de commit
- Las credenciales de Google deben compartirse con el Service Account email

### Google Sheets

- Los empleados pueden aparecer duplicados (mismo ID en ambas hojas)
- El sistema retorna el registro con `FECHA DE INGRESO` más reciente
- Las columnas duplicadas en Google Sheets reciben sufijos (`_1`, `_2`, etc.)

### PDF Generation

- Las coordenadas son en puntos (1/72 pulgada)
- Origen de coordenadas: esquina superior izquierda
- Usar `coordenadas_pdf.py` para encontrar posiciones exactas visualmente
- Los anexos (EMSSANAR) se unen al final del PDF principal

### Campos Especiales

- `TELEFONO_MOVIL`: Si contiene guión, se divide en dos líneas (excepto SANITAS)
- `FECHA_INGRESO`: Se usa para `fecha_nacimiento2` y `fecha_nacimiento3`
- `DEPARTAMENTO_POR_CIUDAD`: Se calcula dinámicamente desde la hoja "Codigo Pais-Dpto-Ciudad"

### Numeración de páginas en el código

Las páginas son **0-indexed** en PyMuPDF. Siempre restar 1 a la página física:

| `'page':` en config | Página física del PDF |
|---|---|
| `0` (o sin `page`) | Página 1 |
| `1` | Página 2 |
| `2` | Página 3 |

`datos_tramite` también respeta `'page': N`, lo que permite poner X's fijas en cualquier página (útil para marcar casillas tipo "CC" en formularios de varias páginas como ASMET SALUD).
