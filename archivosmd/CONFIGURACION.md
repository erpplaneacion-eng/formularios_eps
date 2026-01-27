# 🔧 Guía de Configuración - Formularios EPS

Esta guía te ayudará a configurar el proyecto tanto para desarrollo local como para producción en Railway.

## 📑 Tabla de Contenidos

- [Configuración Rápida Desarrollo](#-configuración-rápida-desarrollo)
- [Configuración Producción Railway](#-configuración-producción-railway)
- [Variables de Entorno](#-variables-de-entorno)
- [Credenciales Google](#-credenciales-google)
- [Base de Datos](#-base-de-datos)
- [Solución de Problemas](#-solución-de-problemas)

---

## 🚀 Configuración Rápida Desarrollo

### 1. Instalar dependencias

```bash
cd formularios_eps
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias de desarrollo (sin PostgreSQL)
pip install -r requirements-dev.txt
```

### 2. Configurar Google Sheets

**Opción A: Archivo JSON (Más fácil)**

1. Descarga credenciales de Google Cloud Console
2. Guarda como: `formularios/service_account.json`
3. ¡Listo! La aplicación lo detectará automáticamente

**Opción B: Variable de entorno**

1. Edita el archivo `.env`
2. Descomenta y completa `GOOGLE_CREDENTIALS`

### 3. Configurar Base de Datos

```bash
cd formularios
python manage.py migrate
python manage.py createsuperuser
```

### 4. Ejecutar

```bash
python manage.py runserver
```

Accede a: http://localhost:8000

---

## 🌐 Configuración Producción Railway

### 1. Conectar Repositorio

- Ve a Railway.app
- New Project > Deploy from GitHub
- Selecciona tu repositorio

### 2. Agregar PostgreSQL

- Add Service > Database > PostgreSQL
- Railway configura `DATABASE_URL` automáticamente

### 3. Configurar Variables de Entorno

En Railway Settings > Variables:

```bash
SECRET_KEY=clave-secreta-aleatoria-muy-larga-y-segura-aqui
DEBUG=False
ALLOWED_HOSTS=tu-proyecto.railway.app
CSRF_TRUSTED_ORIGINS=https://tu-proyecto.railway.app,https://*.railway.app
GOOGLE_CREDENTIALS={"type":"service_account",...}
```

### 4. Deploy

```bash
git push origin main
```

### 5. Primera vez: Ejecutar Migraciones

En Railway Terminal:

```bash
cd formularios && python manage.py migrate && python manage.py createsuperuser
```

---

## 📋 Variables de Entorno

### Tabla Comparativa

| Variable | Desarrollo | Producción | Obligatorio |
|----------|-----------|-----------|-------------|
| `SECRET_KEY` | Auto-generado | Personalizado | ✅ Producción |
| `DEBUG` | `True` (auto) | `False` | ❌ |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Dominio Railway | ✅ Producción |
| `DATABASE_URL` | **NO definir** | Auto Railway | ✅ Producción |
| `GOOGLE_CREDENTIALS` | Opcional (usar archivo) | JSON string | ✅ |
| `CSRF_TRUSTED_ORIGINS` | No requerido | URLs producción | ✅ Producción |

### Detección Automática de Entorno

El proyecto detecta automáticamente si está en desarrollo o producción:

```
¿Existe DATABASE_URL?
├─ SÍ → Modo Producción
│   ├─ DEBUG = False
│   ├─ Base de datos = PostgreSQL
│   └─ Credenciales = GOOGLE_CREDENTIALS (variable)
│
└─ NO → Modo Desarrollo
    ├─ DEBUG = True
    ├─ Base de datos = SQLite
    └─ Credenciales = service_account.json (archivo)
```

---

## 🔐 Credenciales Google

### Obtener Credenciales

1. **Ir a Google Cloud Console**
   - https://console.cloud.google.com/

2. **Crear/Seleccionar Proyecto**
   - Nombre sugerido: "formularios-eps"

3. **Habilitar Google Sheets API**
   - APIs & Services > Enable APIs
   - Buscar: "Google Sheets API"
   - Click: Enable

4. **Crear Service Account**
   - IAM & Admin > Service Accounts
   - Create Service Account
   - Nombre: "formularios-eps-service"
   - Rol: Editor (o Viewer si solo lectura)

5. **Generar Clave JSON**
   - Seleccionar Service Account creado
   - Keys > Add Key > Create new key
   - Tipo: JSON
   - Download

6. **Configurar Permisos del Sheet**
   - Abrir Google Sheet
   - Share
   - Agregar email del Service Account
   - Permiso: Editor (o Viewer)

### Uso en Desarrollo

**Archivo `service_account.json`:**

```bash
# Copiar archivo descargado a:
formularios/service_account.json
```

### Uso en Producción

**Variable `GOOGLE_CREDENTIALS`:**

```bash
# Contenido del JSON en una línea:
GOOGLE_CREDENTIALS='{"type":"service_account","project_id":"...","private_key":"-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n","client_email":"...@....iam.gserviceaccount.com",...}'
```

> **⚠️ IMPORTANTE:** No commitear archivos con credenciales reales. Están protegidos en `.gitignore`.

---

## 💾 Base de Datos

### Desarrollo Local

**SQLite (Automático)**

```bash
# Se crea automáticamente en:
formularios/db.sqlite3

# Migraciones:
python manage.py migrate

# Crear usuario:
python manage.py createsuperuser
```

### Producción Railway

**PostgreSQL (Configuración Automática)**

```bash
# Railway configura automáticamente DATABASE_URL

# Primera vez (en Railway Terminal):
cd formularios && python manage.py migrate
```

### Conectar a BD de Producción desde Local (Opcional)

```bash
# En .env local, agregar:
DATABASE_URL=postgresql://user:password@host:port/database

# Usar DATABASE_PUBLIC_URL de Railway
```

---

## 🐛 Solución de Problemas

### Error: "No se encontraron credenciales de Google"

```bash
# Verificar que exista uno de estos:
# 1. formularios/service_account.json
# 2. Variable GOOGLE_CREDENTIALS en .env

# Solución:
ls formularios/service_account.json
# Si no existe, copiar archivo JSON descargado
```

### Error: "Permission denied" Google Sheets

```bash
# El Service Account no tiene acceso al Sheet

# Solución:
# 1. Abrir Google Sheet
# 2. Share
# 3. Agregar email del Service Account
# 4. Dar permisos de Editor
```

### Error: Base de datos bloqueada (SQLite)

```bash
# Otro proceso está usando db.sqlite3

# Solución:
# 1. Cerrar todos los procesos Django
# 2. Reiniciar terminal
# 3. python manage.py runserver
```

### Error: CSRF verification failed

```bash
# En producción, CSRF_TRUSTED_ORIGINS no configurado

# Solución en Railway Variables:
CSRF_TRUSTED_ORIGINS=https://tu-dominio.railway.app,https://*.railway.app
```

### Error: Module not found

```bash
# Dependencias no instaladas

# Solución:
pip install -r requirements.txt
```

### Error: "DisallowedHost"

```bash
# El host no está en ALLOWED_HOSTS

# Solución en Railway Variables:
ALLOWED_HOSTS=tu-dominio.railway.app,*.railway.app
```

### Error: 500 Internal Server Error en Producción

```bash
# Posibles causas:
# 1. SECRET_KEY no configurado
# 2. GOOGLE_CREDENTIALS inválido
# 3. Migraciones no ejecutadas

# Solución:
# 1. Verificar todas las variables de entorno
# 2. Ver logs en Railway Dashboard
# 3. Ejecutar: cd formularios && python manage.py migrate
```

---

## 📁 Archivos de Configuración

```
formularios_eps/
├── .env                      # Tu configuración local (NO commitear)
├── .env.example              # Plantilla vacía (commitear)
├── .env.development          # Referencia desarrollo (commitear)
├── .env.production.backup    # Backup producción (NO commitear)
├── .gitignore                # Protección archivos sensibles
└── formularios/
    ├── service_account.json  # Credenciales Google (NO commitear)
    └── db.sqlite3            # Base de datos local (NO commitear)
```

### Archivos Protegidos por .gitignore

- `.env` (excepto .env.example y .env.development)
- `service_account.json`
- `credentials.json`
- `db.sqlite3`
- `*.json.key`
- `.env.production.backup`

---

## 🎯 Checklist Desarrollo

- [ ] Clonar repositorio
- [ ] Crear y activar venv
- [ ] Instalar dependencias (`pip install -r requirements.txt`)
- [ ] Obtener credenciales Google Cloud
- [ ] Guardar como `formularios/service_account.json`
- [ ] Compartir Google Sheet con Service Account
- [ ] Ejecutar migraciones (`python manage.py migrate`)
- [ ] Crear superusuario (`python manage.py createsuperuser`)
- [ ] Iniciar servidor (`python manage.py runserver`)
- [ ] Probar login en http://localhost:8000

## 🎯 Checklist Producción

- [ ] Crear proyecto en Railway
- [ ] Conectar repositorio GitHub
- [ ] Agregar servicio PostgreSQL
- [ ] Configurar variable `SECRET_KEY`
- [ ] Configurar variable `ALLOWED_HOSTS`
- [ ] Configurar variable `CSRF_TRUSTED_ORIGINS`
- [ ] Configurar variable `GOOGLE_CREDENTIALS`
- [ ] Configurar variable `DEBUG=False`
- [ ] Deploy automático (git push)
- [ ] Ejecutar migraciones en Railway Terminal
- [ ] Crear superusuario en Railway Terminal
- [ ] Probar en https://tu-proyecto.railway.app

---

## 💡 Tips

### Desarrollo Local

```bash
# Ver variables de entorno cargadas
python -c "import os; print(os.environ.get('DEBUG'))"

# Limpiar base de datos y empezar de cero
rm formularios/db.sqlite3
python manage.py migrate
python manage.py createsuperuser

# Recopilar archivos estáticos
python manage.py collectstatic --noinput
```

### Producción Railway

```bash
# Ver logs en tiempo real
railway logs

# Ejecutar comando en producción
railway run python manage.py migrate

# Variables de entorno
railway variables
```

---

**¿Necesitas más ayuda?**

- 📖 Ver [README.md](README.md) completo
- 🐛 Reportar issue en GitHub
- 📧 Contactar equipo de desarrollo CHVS
