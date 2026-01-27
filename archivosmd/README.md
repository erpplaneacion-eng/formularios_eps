# Sistema de Formularios EPS - CHVS

Sistema web para la generación automática de formularios de afiliación a EPS (Entidades Promotoras de Salud) para la corporación "Hacia un Valle Solidario" (CHVS).

## 📋 Características

- **Autenticación de usuarios** - Sistema de login seguro con Django Auth
- **Búsqueda de empleados** - Consulta por cédula en base de datos Google Sheets
- **Generación automática de PDFs** - Llenado de formularios EPS con datos del empleado
- **Multi-EPS** - Soporte para múltiples aseguradoras de salud
- **Integración Google Sheets** - Datos sincronizados en tiempo real
- **Configuración dual** - Funciona en desarrollo local y producción Railway

## 🛠️ Stack Tecnológico

- **Backend:** Django 5.2.7 + Python 3.11.9
- **Base de Datos:** PostgreSQL (producción) / SQLite (desarrollo)
- **Integración:** Google Sheets API (gspread)
- **Generación PDFs:** PyMuPDF (fitz)
- **Servidor:** Gunicorn + WhiteNoise
- **Deploy:** Railway.app

## 📁 Estructura del Proyecto

```
formularios_eps/
├── formularios/                  # Proyecto Django
│   ├── formularios/              # Configuración Django
│   │   ├── settings.py           # Configuración principal
│   │   ├── urls.py               # URLs principales
│   │   └── wsgi.py               # WSGI application
│   ├── formatos_eps/             # Aplicación principal
│   │   ├── views.py              # Vistas de la aplicación
│   │   ├── google_sheets.py      # Integración Google Sheets
│   │   ├── pdf_generator.py      # Generación de PDFs
│   │   └── templates/            # Plantillas HTML
│   ├── manage.py                 # Script administración Django
│   └── db.sqlite3                # Base de datos SQLite (desarrollo)
├── formatos/                     # Plantillas PDF de formularios EPS
├── .env                          # Variables de entorno (desarrollo)
├── .env.example                  # Plantilla de variables de entorno
├── .env.development              # Referencia para desarrollo
├── .env.production.backup        # Backup de configuración producción
├── .gitignore                    # Archivos ignorados por Git
├── requirements.txt              # Dependencias Python
├── runtime.txt                   # Versión de Python
└── railway.json                  # Configuración Railway
```

## 🚀 Configuración para Desarrollo Local

### Requisitos Previos

- Python 3.11.9
- pip
- Git
- Cuenta de Google Cloud con Google Sheets API habilitado

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/erpplaneacion-eng/formularios_eps.git
cd formularios_eps/formularios_eps
```

### Paso 2: Crear Entorno Virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
# Para desarrollo local (sin PostgreSQL)
pip install -r requirements-dev.txt

# O si quieres todas las dependencias (puede fallar psycopg2 en Windows):
# pip install -r requirements.txt
```

### Paso 4: Configurar Variables de Entorno

El proyecto ya incluye un archivo `.env` configurado para desarrollo local. Solo necesitas agregar las credenciales de Google.

**Opción 1: Usar archivo service_account.json (Recomendado para desarrollo)**

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Selecciona tu proyecto o crea uno nuevo
3. Habilita **Google Sheets API**:
   - API & Services > Enable APIs and Services
   - Busca "Google Sheets API" y habilítala
4. Crea Service Account:
   - IAM & Admin > Service Accounts
   - Create Service Account
   - Asigna rol "Editor" o permisos de Google Sheets
5. Genera clave JSON:
   - Selecciona la Service Account
   - Keys > Add Key > Create new key > JSON
   - Descarga el archivo
6. Guarda el archivo como: `formularios/service_account.json`
7. Comparte tu Google Sheet con el email del Service Account

**Opción 2: Usar variable de entorno GOOGLE_CREDENTIALS**

Edita `.env` y descomenta la línea `GOOGLE_CREDENTIALS`, agregando el JSON completo en una sola línea.

### Paso 5: Configurar Base de Datos

```bash
cd formularios
python manage.py migrate
python manage.py createsuperuser
```

Sigue las instrucciones para crear tu usuario administrador.

### Paso 6: Iniciar Servidor de Desarrollo

```bash
python manage.py runserver
```

Accede a: [http://localhost:8000](http://localhost:8000)

### Paso 7: Probar la Aplicación

1. Inicia sesión con las credenciales creadas
2. Busca un empleado por cédula
3. Genera el PDF del formulario EPS

## 🌐 Configuración para Producción (Railway)

### Paso 1: Crear Proyecto en Railway

1. Ve a [Railway.app](https://railway.app)
2. Conecta tu repositorio de GitHub
3. Railway detectará automáticamente el proyecto Django

### Paso 2: Configurar Variables de Entorno

En Railway, agrega las siguientes variables:

```bash
# Django
SECRET_KEY=tu-clave-secreta-aleatoria-muy-larga
DEBUG=False
ALLOWED_HOSTS=tu-dominio.railway.app
CSRF_TRUSTED_ORIGINS=https://tu-dominio.railway.app,https://*.railway.app

# Database (Railway la configura automáticamente)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Google Credentials (JSON completo en una línea)
GOOGLE_CREDENTIALS={"type":"service_account","project_id":"...","private_key":"..."}
```

### Paso 3: Agregar PostgreSQL

1. En Railway, agrega un nuevo servicio: PostgreSQL
2. Railway configurará automáticamente `DATABASE_URL`

### Paso 4: Deploy

```bash
git push origin main
```

Railway desplegará automáticamente.

### Paso 5: Ejecutar Migraciones (Primera vez)

Accede a la terminal de Railway y ejecuta:

```bash
cd formularios && python manage.py migrate && python manage.py createsuperuser
```

## 🔧 Configuración Avanzada

### Variables de Entorno

| Variable | Desarrollo | Producción | Descripción |
|----------|-----------|-----------|-------------|
| `SECRET_KEY` | Valor por defecto | **Requerido** | Clave secreta Django |
| `DEBUG` | `True` (auto) | `False` | Modo debug |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Dominio Railway | Hosts permitidos |
| `DATABASE_URL` | No definir (SQLite) | PostgreSQL URL | URL base de datos |
| `GOOGLE_CREDENTIALS` | service_account.json | JSON string | Credenciales Google |
| `CSRF_TRUSTED_ORIGINS` | No requerido | URLs de producción | Orígenes CSRF |

### Detección Automática de Entorno

El proyecto detecta automáticamente el entorno:

- **Si existe `DATABASE_URL`** → Producción (DEBUG=False, PostgreSQL)
- **Si NO existe `DATABASE_URL`** → Desarrollo (DEBUG=True, SQLite)

### Google Sheets

**Spreadsheet ID:** `1OzyM4jlADde1MKU7INbtXvVOUaqD1KfZH_gFLOciwNk`

**Hojas utilizadas:**
- `Planta` - Empleados de planta
- `Manipuladoras` - Manipuladoras de alimentos

**Columnas requeridas:**
- CEDULA
- PRIMER APELLIDO
- SEGUNDO APELLIDO
- NOMBRES
- FECHA DE NACIMIENTO
- PAIS DE NACIMIENTO
- CODIGO SEXO
- DEPARTAMENTO NACIMIENTO
- CIUDAD DE NACIMIENTO
- EPS

### EPSs Soportadas

1. COMFENALCO VALLE ✅ (Activo con plantilla PDF)
2. SURA
3. SOS
4. SANITAS
5. EMSSANAR
6. SALUD TOTAL
7. ASMET SALUD
8. NUEVA EPS
9. ASOCIACION MUTUAL SER EMPRESA SOLIDARIA DE SALUD EPS-S
10. FAMISANAR
11. COOSALUD
12. ENTIDAD PROMOTORA DE SALUD MALLAMAS EPSI
13. COMPENSAR
14. A.I.C.

> **Nota:** Solo COMFENALCO VALLE tiene plantilla PDF configurada. Para agregar más, coloca el PDF en `formatos/` y configura en `pdf_generator.py`.

## 📝 Scripts Útiles

```bash
# Listar usuarios
python list_users.py

# Probar conexión Google Sheets
python test_google_sheets.py

# Probar generación de PDFs
python test_pdf_generation.py

# Buscar columnas en Google Sheets
python buscar_columnas.py
```

## 🐛 Solución de Problemas

### Error: "No se encontraron credenciales de Google"

**Solución:**
- Asegúrate de tener `service_account.json` en `formularios/`
- O define `GOOGLE_CREDENTIALS` en `.env`

### Error: Base de datos bloqueada (SQLite)

**Solución:**
- Cierra otros procesos que usen `db.sqlite3`
- Reinicia el servidor

### Error: CSRF verification failed

**Solución:**
- En producción, configura `CSRF_TRUSTED_ORIGINS` con tu dominio
- En desarrollo, asegúrate de usar `localhost:8000`

### Error: Módulo no encontrado

**Solución:**
```bash
pip install -r requirements.txt
```

## 📚 Recursos

- [Documentación Django](https://docs.djangoproject.com/)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [Railway Documentation](https://docs.railway.app/)

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

## 👥 Autores

**Corporación Hacia un Valle Solidario (CHVS)**
- Desarrollo y mantenimiento

---

**¿Preguntas o problemas?** Abre un issue en GitHub.
