# GEMINI.md - Contexto del Proyecto "Formularios EPS"

Este archivo sirve como memoria y guía para agentes de IA (y desarrolladores) que trabajen en este proyecto.

## 1. Resumen del Proyecto
**Nombre:** `formularios_eps`
**Propósito:** Sistema web para generar automáticamente formularios de afiliación a EPS (Entidades Promotoras de Salud) en formato PDF, precargados con datos de empleados obtenidos desde Google Sheets.
**Organización:** Corporación Hacia un Valle Solidario (CHVS).

## 2. Arquitectura y Stack Tecnológico
*   **Backend:** Django 5.2.7 (Python 3.11).
*   **Base de Datos:**
    *   *Desarrollo:* SQLite (`db.sqlite3`).
    *   *Producción:* PostgreSQL (Railway).
*   **PDF Engine:** `PyMuPDF` (módulo `fitz`). Inyecta texto y marcas (X) sobre plantillas PDF existentes.
*   **Fuente de Datos:** Google Sheets API (librería `gspread`). Lee de hojas "Planta" y "Manipuladoras".
*   **Infraestructura:** Railway (PaaS). Usa `gunicorn` + `whitenoise`.
*   **Autenticación:** Django Auth estándar.

## 3. Estructura de Archivos Clave

| Ruta | Descripción |
| :--- | :--- |
| `formularios/formatos_eps/pdf_generator.py` | **Núcleo Lógico.** Contiene `CONFIGURACION_FORMATOS` (mapeo de coordenadas X,Y por EPS) y la función `rellenar_pdf_empleado`. |
| `formularios/formatos_eps/views.py` | **Controladores.** Maneja Login, Búsqueda (`find_row_by_cedula`) y Descarga de PDF. |
| `formularios/formatos_eps/google_sheets.py` | **Integración.** Lógica para conectar y buscar en Google Sheets. |
| `formularios/formularios/settings.py` | **Configuración.** Detecta entorno (Dev vs Prod) basado en `DATABASE_URL`. |
| `formatos/` | **Recursos.** Directorio que almacena las plantillas PDF bases (e.g., `formulario_comfenalco.pdf`). |
| `list_users.py` / `test_*.py` | **Scripts Utilitarios.** Scripts raíz para debug y mantenimiento fuera de Django. |

## 4. Flujo de Datos
1.  **Usuario** inicia sesión y busca una cédula.
2.  **Django** llama a `google_sheets.py` para buscar la fila en el Spreadsheet ID configurado.
3.  **Sistema** normaliza los datos (nombres, fechas, EPS, salario, etc.).
4.  **Usuario** hace clic en "Generar PDF".
5.  **Django** llama a `pdf_generator.py`:
    *   Identifica la EPS del empleado.
    *   Carga la plantilla PDF correspondiente desde `formatos/`.
    *   Busca las coordenadas (X, Y) en `CONFIGURACION_FORMATOS`.
    *   Escribe texto y marca "X" en las casillas.
    *   Adjunta anexos si están configurados.
6.  **Usuario** recibe el PDF generado como descarga.

## 5. Configuración y Variables de Entorno
El proyecto usa `.env` (local) y Variables de Railway (producción).

*   `GOOGLE_CREDENTIALS`: JSON completo de la Service Account (o archivo `service_account.json` en local).
*   `DATABASE_URL`: URL de conexión a Postgres (Auto en Railway).
*   `SECRET_KEY`: Llave de seguridad Django.
*   `ALLOWED_HOSTS`: Dominios permitidos.
*   `CSRF_TRUSTED_ORIGINS`: Para evitar errores CSRF en producción (HTTPS).

## 6. Guía para Tareas Comunes

### A. Agregar una Nueva EPS
Para soportar una nueva EPS (ej: "NUEVA EPS"):
1.  **Conseguir el PDF:** Obtener el formulario oficial digital y colocarlo en `formatos/`.
2.  **Mapear Coordenadas:** Usar `coordenadas_pdf.py` (si existe) o herramientas externas para obtener coordenadas X,Y de cada campo.
3.  **Actualizar `pdf_generator.py`:**
    *   Agregar entrada en `CONFIGURACION_FORMATOS` bajo la clave exacta que viene del Google Sheet (ej: `'NUEVA EPS'`).
    *   Definir `'archivo'`: nombre del PDF en `formatos/`.
    *   Definir `'campos'`: Diccionario mapeando campos de datos (`CEDULA`, `NOMBRES`, etc.) a `{x: 123, y: 456}`.
4.  **Probar:** Usar un script de prueba o la interfaz web para verificar la alineación.

### B. Debug de Google Sheets
Si la búsqueda falla:
*   Verificar que la Service Account tenga permiso de "Editor" o "Lector" en el Sheet.
*   Ejecutar `python test_google_sheets.py` para aislar el problema de conexión.
*   Revisar nombres de columnas en el Sheet; deben coincidir con lo esperado en el código (o ser normalizados).

### C. Despliegue en Railway
*   Push a rama `main` dispara deploy.
*   Asegurarse de que `requirements.txt` esté actualizado.
*   Si hay cambios en modelos (poco común aquí), ejecutar migraciones en la consola de Railway.

## 7. Convenciones de Desarrollo
*   **Idioma:** Código y comentarios preferiblemente en Español (dado el contexto del cliente CHVS), aunque el framework use inglés.
*   **Manejo de Errores:** Siempre capturar excepciones en generación de PDF para no tumbar el server; usar `messages.error` para avisar al usuario.
*   **No Hardcoding:** Credenciales y Nits sensibles deben ir en variables de entorno o diccionarios de configuración, no dispersos en el código.
