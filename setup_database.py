"""
Script para aplicar migraciones y crear usuarios en la base de datos de PostgreSQL de Railway
"""
import os
import sys
import django
from pathlib import Path

# Configurar el path al proyecto Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / 'formularios'))

# Cargar variables de entorno desde .env
from dotenv import load_dotenv
load_dotenv(BASE_DIR / '.env')

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formularios.settings')
django.setup()

# Importar despues de configurar Django
from django.core.management import call_command
from django.contrib.auth.models import User

def aplicar_migraciones():
    """Aplica las migraciones de Django"""
    print("=" * 60)
    print("APLICANDO MIGRACIONES")
    print("=" * 60)

    try:
        # Crear migraciones si hay cambios
        print("\n1. Generando archivos de migracion...")
        call_command('makemigrations')

        # Aplicar migraciones
        print("\n2. Aplicando migraciones a la base de datos...")
        call_command('migrate')

        print("\n[OK] Migraciones aplicadas exitosamente")
        return True
    except Exception as e:
        print(f"\n[ERROR] Error al aplicar migraciones: {str(e)}")
        return False

def crear_usuario(username, password, is_superuser=False):
    """Crea un usuario en la base de datos"""
    try:
        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            print(f"  [WARN] Usuario '{username}' ya existe. Actualizando contrasena...")
            user = User.objects.get(username=username)
            user.set_password(password)
            if is_superuser:
                user.is_superuser = True
                user.is_staff = True
            user.save()
            print(f"  [OK] Usuario '{username}' actualizado")
        else:
            # Crear nuevo usuario
            if is_superuser:
                user = User.objects.create_superuser(
                    username=username,
                    password=password,
                    email=f'{username}@formularios-eps.local'
                )
                print(f"  [OK] Superusuario '{username}' creado exitosamente")
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=f'{username}@formularios-eps.local'
                )
                print(f"  [OK] Usuario '{username}' creado exitosamente")

        return True
    except Exception as e:
        print(f"  [ERROR] Error al crear usuario '{username}': {str(e)}")
        return False

def main():
    print("\n" + "=" * 60)
    print("CONFIGURACION DE BASE DE DATOS - FORMULARIOS EPS")
    print("=" * 60)

    # Verificar variables de entorno
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("\n[ERROR] No se encontro DATABASE_URL en las variables de entorno")
        print("  Asegurese de que el archivo .env este configurado correctamente")
        return

    print(f"\n[INFO] Base de datos: {database_url[:30]}...")

    # 1. Aplicar migraciones
    if not aplicar_migraciones():
        print("\n[WARN] Continuando con la creacion de usuarios a pesar del error...")

    # 2. Crear usuarios
    print("\n" + "=" * 60)
    print("CREANDO USUARIOS")
    print("=" * 60)

    print("\n1. Creando usuario 'erwin'...")
    crear_usuario('erwin', 'erwin123', is_superuser=False)

    print("\n2. Creando usuario 'admin'...")
    crear_usuario('admin', 'admin123', is_superuser=True)

    print("\n" + "=" * 60)
    print("PROCESO COMPLETADO")
    print("=" * 60)
    print("\n[OK] Configuracion finalizada exitosamente")
    print("\nUsuarios creados:")
    print("  - erwin (usuario normal)")
    print("  - admin (superusuario)")
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
