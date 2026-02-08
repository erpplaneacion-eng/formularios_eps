# GEMINI.md - Contexto y Guía del Proyecto "Formularios EPS"

Este archivo centraliza el contexto, arquitectura y flujos de trabajo para el desarrollo del proyecto.

## 1. Resumen del Proyecto
**Nombre:** `formularios_eps` (CHVS)
**Propósito:** Automatizar la generación de formularios de afiliación a EPS (Entidades Promotoras de Salud) en formato PDF. El sistema extrae datos de empleados desde Google Sheets y los inyecta en plantillas PDF oficiales de cada EPS.
**Organización:** Corporación Hacia un Valle Solidario (CHVS).

## 2. Stack Tecnológico
*   **Lenguaje:** Python 3.11.9
*   **Framework:** Django 5.2.7
*   **Base de Datos:**
    *   *Desarrollo:* SQLite (`formularios/db.sqlite3`)
    *   *Producción:* PostgreSQL (Railway)
*   **PDF Engine:** `PyMuPDF` (módulo `fitz`) para manipulación y llenado de PDFs.
*   **Integración:** Google Sheets API (`gspread`) para lectura de datos en tiempo real.
*   **Infraestructura:** Railway (PaaS) con Gunicorn y WhiteNoise.

## 3. Estructura del Proyecto

```text
C:\Users\User\OneDrive\Desktop\CHVS\FORMULARIOS_EPS\formularios_eps
├── formatos/           # Plantillas PDF base (oficiales de las EPS).
├── formularios/        # Directorio raíz de Django.
│   ├── formularios/    # Configuración de Django (settings, urls).
│   ├── formatos_eps/   # App principal (lógica de negocio).
│   │   ├── google_sheets.py  # Conexión y búsqueda en Sheets.
│   │   ├── pdf_generator.py  # Lógica de mapeo y generación de PDF.
│   │   └── views.py          # Controladores (Login, Búsqueda, Descarga).
│   └── manage.py       # Utilidad de Django.
├── test/               # Scripts de prueba y utilitarios de diagnóstico.
├── requirements.txt    # Dependencias del proyecto.
└── runtime.txt         # Versión de Python.
```

## 4. Configuración y Entorno

El sistema detecta el entorno automáticamente basado en la presencia de la variable `DATABASE_URL`.

### Variables Clave:
- `GOOGLE_CREDENTIALS`: JSON de la cuenta de servicio (Producción).
- `GOOGLE_SHEET_ID`: ID del Spreadsheet de Google Sheets.
- `SECRET_KEY`: Llave secreta de Django.
- `DATABASE_URL`: URL de conexión a PostgreSQL (Producción).

### Archivos de Credenciales (Local):
- `.env`: Variables de entorno.
- `formularios/service_account.json`: Credenciales de Google API.

## 5. Flujo de Datos Principal

1.  **Dashboard:** Tras el login, el usuario accede a un panel centralizado con módulos de Gestión Humana.
2.  **Búsqueda:** Al seleccionar "Formularios EPS", se ingresa una cédula. El sistema consulta `google_sheets.py`.
3.  **Extracción:** Se busca en las hojas "Planta" y "Manipuladoras". Se normalizan los datos (Nombres, EPS, Salario, etc.).
4.  **Mapeo:** Al generar el PDF, `pdf_generator.py` usa `CONFIGURACION_FORMATOS` para encontrar las coordenadas (X, Y) correspondientes a la EPS del empleado.
5.  **Inyección:** Se usa `PyMuPDF` para escribir texto y marcar "X" en la plantilla PDF de `formatos/`.
6.  **Descarga:** El usuario recibe el PDF diligenciado.

## 6. Interfaz de Usuario (UI/UX)
*   **Login:** Diseño moderno con *Glassmorphism* (efecto cristal), fondo de video dinámico y alineación lateral.
*   **Dashboard:** Sistema de tarjetas (Cards) para navegación intuitiva entre módulos internos y externos.
*   **Estilos:** Uso de degradados institucionales y tipografía limpia para una experiencia profesional.

## 7. Guía de Desarrollo
### Comandos Clave:
```bash
# Activar venv (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Correr servidor local
cd formularios
python manage.py runserver

# Correr tests de generación de PDF
python test/test_pdf_generation.py
```

### Agregar una Nueva EPS:
1.  Subir el PDF limpio a `formatos/`.
2.  Mapear coordenadas (X, Y) de cada campo usando herramientas de inspección de PDF.
3.  Actualizar `CONFIGURACION_FORMATOS` en `formularios/formatos_eps/pdf_generator.py`.
4.  Definir el nombre exacto de la EPS tal como aparece en Google Sheets.

### Convenciones:
*   **Idioma:** Código y lógica de negocio preferiblemente en **Español**.
*   **Rutas:** Usar `Pathlib` o rutas relativas a `BASE_DIR`.
*   **Errores:** Capturar excepciones en la generación de PDF y usar `django.contrib.messages` para notificar al usuario.

---
Para más detalles históricos, consultar `.gemini/GEMINI.md` o `archivosmd/README.md`.
