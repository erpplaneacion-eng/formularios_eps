# GEMINI.md - Contexto y Guía del Proyecto "Formularios EPS"

Este archivo define el contexto, arquitectura y flujos de trabajo para agentes de IA que operan en este proyecto.

## 1. Resumen del Proyecto
**Nombre:** `formularios_eps` (CHVS)
**Propósito:** Sistema web automatizado para generar formularios de afiliación a EPS (Entidades Promotoras de Salud) en formato PDF. El sistema extrae datos de empleados desde Google Sheets y los inyecta en plantillas PDF oficiales.
**Organización:** Corporación Hacia un Valle Solidario (CHVS).

## 2. Stack Tecnológico
*   **Lenguaje:** Python 3.11.9
*   **Framework:** Django 5.2.7
*   **Base de Datos:**
    *   *Local:* SQLite (`formularios/db.sqlite3`)
    *   *Producción:* PostgreSQL (Railway)
*   **PDF Engine:** `PyMuPDF` (módulo `fitz`) para manipulación de PDFs.
*   **Integración:** Google Sheets API (`gspread`) para lectura de datos.
*   **Servidor:** Gunicorn + WhiteNoise.
*   **Infraestructura:** Railway (PaaS).

## 3. Estructura y Archivos Clave

### Rutas Importantes
| Ruta Relativa | Descripción |
| :--- | :--- |
| `formularios/` | Raíz del proyecto Django. |
| `formularios/manage.py` | Script de gestión de Django. |
| `formularios/formularios/settings.py` | Configuración principal. Detecta entorno (Dev/Prod). |
| `formularios/formatos_eps/` | **App Principal.** Contiene toda la lógica de negocio. |
| `formularios/formatos_eps/pdf_generator.py` | **Core Logic.** Mapeo de coordenadas (X,Y) y llenado de PDFs. |
| `formularios/formatos_eps/google_sheets.py` | Lógica de conexión y búsqueda en Google Sheets. |
| `formatos/` | Almacenamiento de plantillas PDF base (e.g., `formulario_comfenalco.pdf`). |
| `requirements.txt` | Dependencias del proyecto (Raíz). |
| `runtime.txt` | Versión de Python (Raíz). |
| `otros/` | Archivos varios (backups, tests manuales). |
| `archivosmd/` | Documentación humana detallada (README, SETUP, etc.). |

### Archivos de Configuración
- `.env`: Variables de entorno locales (NO commitear).
- `railway.json` / `Procfile`: Configuración de despliegue en Railway.
- `formularios/service_account.json`: Credenciales de Google (Local).

## 4. Flujo de Datos y Lógica de Negocio

### Generación de Formularios
1.  **Input:** Usuario ingresa una Cédula.
2.  **Búsqueda:**
    - Se consulta `google_sheets.py`.
    - Busca en hojas "Planta" y "Manipuladoras" del Spreadsheet ID configurado.
    - Retorna dict con datos normalizados (Nombres, EPS, Salario, etc.).
3.  **Procesamiento:**
    - El usuario confirma y da clic en "Generar PDF".
    - `pdf_generator.py` selecciona la plantilla en `formatos/` basada en la EPS.
    - Usa `CONFIGURACION_FORMATOS` para mapear datos a coordenadas (X, Y).
    - Inyecta texto y marcas "X" usando `PyMuPDF`.
4.  **Output:** Descarga del PDF diligenciado.

### Detección de Entorno
El archivo `settings.py` usa la variable `DATABASE_URL` como switch:
- **Si existe:** Asume Producción (Debug=False, Postgres).
- **Si NO existe:** Asume Desarrollo (Debug=True, SQLite).

## 5. Guía Operativa

### Instalación y Ejecución Local
```bash
# Activar entorno virtual (Windows)
venv\Scripts\activate

# Instalar dependencias (Nota la ruta)
pip install -r otros/requirements.txt

# Ejecutar servidor
cd formularios
python manage.py runserver
```

### Pruebas y Scripts
Scripts ubicados en la raíz y en `test/` para depuración aislada:
- `python list_users.py`: Lista usuarios desde Google Sheets (prueba de conexión).
- `python test/test_pdf_generation.py`: Genera un PDF de prueba sin levantar el server.
- `python test/buscar_columnas.py`: Herramienta para inspeccionar headers en Sheets.

## 6. Convenciones de Desarrollo
*   **Idioma:** Código, variables y comentarios en **Español**.
*   **Rutas:** No usar rutas absolutas. Usar `pathlib` o `os.path` relativo a `BASE_DIR`.
*   **Logs:** Usar `print` solo para debug local efímero. Usar `logging` o mensajes de error de Django para producción.
*   **Manejo de Errores:** La generación de PDF nunca debe romper el ciclo de vida de la request. Capturar excepciones y mostrar `messages.error`.

## 7. Tareas Comunes (Agente IA)
*   **Nueva EPS:**
    1. Agregar PDF limpio a `formatos/`.
    2. Obtener coordenadas de campos.
    3. Agregar entrada a `CONFIGURACION_FORMATOS` en `pdf_generator.py`.
*   **Error de Columnas:** Si Google Sheets cambia nombres de columnas, actualizar el mapeo en `google_sheets.py`.
*   **Deploy:** Push a `main` despliega automáticamente en Railway.
