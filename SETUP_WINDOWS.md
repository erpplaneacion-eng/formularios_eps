# 🪟 Configuración Rápida - Windows

Guía paso a paso para configurar el proyecto en Windows.

## ⚡ Instalación Rápida

### 1. Abrir PowerShell en el directorio del proyecto

```powershell
# Opción A: Desde el explorador de archivos
# - Navega a: C:\Users\User\OneDrive\Desktop\CHVS\FORMULARIOS_EPS\formularios_eps
# - Shift + Click derecho en carpeta vacía
# - "Abrir ventana de PowerShell aquí" o "Abrir en Terminal"

# Opción B: Desde PowerShell
cd "C:\Users\User\OneDrive\Desktop\CHVS\FORMULARIOS_EPS\formularios_eps"
```

### 2. Crear y activar entorno virtual

```powershell
# Crear entorno virtual (si no existe)
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\activate

# Deberías ver (venv) al inicio de la línea
```

### 3. Instalar dependencias (SIN PostgreSQL)

```powershell
# Usar requirements-dev.txt para desarrollo local
pip install -r requirements-dev.txt
```

**⚠️ NO uses `requirements.txt`** - contiene `psycopg2-binary` que falla en Windows con Python 3.13.

### 4. Configurar credenciales de Google

**Opción A: Archivo JSON (Recomendado)**

1. Descarga credenciales de [Google Cloud Console](https://console.cloud.google.com/)
2. Guarda el archivo como: `formularios\service_account.json`

```powershell
# Verificar que el archivo existe:
dir formularios\service_account.json
```

**Opción B: Variable de entorno**

Edita `.env` y configura `GOOGLE_CREDENTIALS`.

### 5. Configurar base de datos

```powershell
# Navegar a directorio Django
cd formularios

# Crear base de datos SQLite
python manage.py migrate

# Crear usuario administrador
python manage.py createsuperuser
```

Sigue las instrucciones:
- Username: `admin` (o el que prefieras)
- Email: tu email
- Password: tu contraseña

### 6. Iniciar servidor

```powershell
# Iniciar servidor de desarrollo
python manage.py runserver
```

**✅ Listo!** Accede a: http://localhost:8000

### 7. Probar la aplicación

1. Ve a: http://localhost:8000
2. Inicia sesión con las credenciales creadas
3. Busca un empleado por cédula
4. Genera un PDF

---

## 🐛 Solución de Problemas

### Error: "python no se reconoce"

**Solución:**
```powershell
# Usar py en lugar de python
py -m venv venv
.\venv\Scripts\activate
py -m pip install -r requirements-dev.txt
```

### Error: "No se puede ejecutar scripts en este sistema"

**Solución:**
```powershell
# Ejecutar como administrador y cambiar política de ejecución
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Luego intenta activar el venv nuevamente
.\venv\Scripts\activate
```

### Error: "psycopg2-binary failed to build"

**Solución:**
```powershell
# NO uses requirements.txt, usa requirements-dev.txt
pip install -r requirements-dev.txt
```

En desarrollo local usas SQLite, NO PostgreSQL.

### Error: "No module named 'gspread'"

**Solución:**
```powershell
# Asegúrate de tener el venv activado (debe aparecer (venv))
.\venv\Scripts\activate

# Instala las dependencias
pip install -r requirements-dev.txt
```

### Error: "No se encontraron credenciales de Google"

**Solución:**
```powershell
# Verifica que existe el archivo:
dir formularios\service_account.json

# Si no existe, descárgalo de Google Cloud Console
# y guárdalo en: formularios\service_account.json
```

### Error: "DisallowedHost at /"

**Solución:**

Edita `.env` y asegúrate de tener:
```
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Error: Base de datos bloqueada

**Solución:**
```powershell
# Cierra todos los servidores Django
# Ctrl+C en todas las ventanas de PowerShell

# Reinicia el servidor
python manage.py runserver
```

---

## 📋 Checklist de Instalación

- [ ] PowerShell abierto en directorio del proyecto
- [ ] Entorno virtual creado (`python -m venv venv`)
- [ ] Entorno virtual activado (`.\venv\Scripts\activate`)
- [ ] Dependencias instaladas (`pip install -r requirements-dev.txt`)
- [ ] Credenciales Google en `formularios\service_account.json`
- [ ] Migraciones ejecutadas (`python manage.py migrate`)
- [ ] Superusuario creado (`python manage.py createsuperuser`)
- [ ] Servidor iniciado (`python manage.py runserver`)
- [ ] Acceso a http://localhost:8000 ✅

---

## 🎯 Comandos de Uso Diario

### Iniciar desarrollo

```powershell
# 1. Navegar al proyecto
cd "C:\Users\User\OneDrive\Desktop\CHVS\FORMULARIOS_EPS\formularios_eps"

# 2. Activar venv
.\venv\Scripts\activate

# 3. Ir a directorio Django
cd formularios

# 4. Iniciar servidor
python manage.py runserver
```

### Detener servidor

```powershell
# Presionar: Ctrl + C
```

### Ver usuarios en la BD

```powershell
python ..\list_users.py
```

### Limpiar base de datos y empezar de cero

```powershell
# ⚠️ ESTO BORRARÁ TODOS LOS DATOS
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Probar conexión con Google Sheets

```powershell
cd ..
python test_google_sheets.py
```

---

## 📁 Estructura de Archivos

```
formularios_eps/
├── venv/                          # Entorno virtual (NO commitear)
├── formularios/
│   ├── manage.py                  # Script administración Django
│   ├── db.sqlite3                 # Base de datos local (NO commitear)
│   ├── service_account.json       # Credenciales Google (NO commitear)
│   ├── formatos_eps/              # Aplicación principal
│   └── formularios/               # Configuración Django
├── .env                           # Variables de entorno (NO commitear)
├── requirements-dev.txt           # ⭐ Usar este para desarrollo
├── requirements.txt               # Para producción (Railway)
└── README.md                      # Documentación completa
```

---

## 💡 Tips para Windows

### Alias útiles

Crea un archivo `start.ps1` en la raíz del proyecto:

```powershell
# start.ps1
.\venv\Scripts\activate
cd formularios
python manage.py runserver
```

Luego solo ejecuta:
```powershell
.\start.ps1
```

### Accesos directos

1. Crea acceso directo a PowerShell
2. Propiedades > Iniciar en: `C:\Users\User\OneDrive\Desktop\CHVS\FORMULARIOS_EPS\formularios_eps`
3. ¡Doble click y listo!

---

## 🔗 Enlaces Útiles

- **Aplicación local**: http://localhost:8000
- **Admin Django**: http://localhost:8000/admin
- **Google Cloud Console**: https://console.cloud.google.com/
- **Documentación completa**: Ver [README.md](README.md)
- **Guía de configuración**: Ver [CONFIGURACION.md](CONFIGURACION.md)

---

**¿Problemas?** Revisa la sección de troubleshooting o consulta [CONFIGURACION.md](CONFIGURACION.md).
