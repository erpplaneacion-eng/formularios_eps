"""
Script para verificar los usuarios creados en la base de datos
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
from django.contrib.auth.models import User

def verificar_usuarios():
    """Verifica y lista los usuarios en la base de datos"""
    print("\n" + "=" * 60)
    print("USUARIOS EN LA BASE DE DATOS")
    print("=" * 60)

    usuarios = User.objects.all().order_by('username')

    if not usuarios:
        print("\n[WARN] No hay usuarios en la base de datos")
        return

    print(f"\n[INFO] Total de usuarios: {usuarios.count()}\n")

    for usuario in usuarios:
        print(f"Usuario: {usuario.username}")
        print(f"  - Email: {usuario.email}")
        print(f"  - Es superusuario: {'Si' if usuario.is_superuser else 'No'}")
        print(f"  - Es staff: {'Si' if usuario.is_staff else 'No'}")
        print(f"  - Esta activo: {'Si' if usuario.is_active else 'No'}")
        print(f"  - Fecha de creacion: {usuario.date_joined}")
        print()

    print("=" * 60)

if __name__ == '__main__':
    verificar_usuarios()
