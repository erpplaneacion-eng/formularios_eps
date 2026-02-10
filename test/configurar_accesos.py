import os
import django
import sys

# Añadir el directorio del proyecto al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'formularios'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formularios.settings')
django.setup()

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType

def setup_access_control():
    print("Configurando grupos y permisos de acceso...")
    
    # Definir los grupos y sus permisos correspondientes
    grupos_config = {
        'Acceso EPS': ['ver_eps'],
        'Acceso Certificados': ['ver_certificados'],
        'Acceso Incapacidades': ['ver_incapacidades'],
    }
    
    for nombre_grupo, codigos_permiso in grupos_config.items():
        grupo, created = Group.objects.get_or_create(name=nombre_grupo)
        if created:
            print(f"Grupo creado: {nombre_grupo}")
        else:
            print(f"Grupo ya existe: {nombre_grupo}")
            
        # Asignar permisos al grupo
        for cod_permiso in codigos_permiso:
            try:
                permiso = Permission.objects.get(codename=cod_permiso, content_type__app_label='formatos_eps')
                grupo.permissions.add(permiso)
                print(f"  Permiso '{cod_permiso}' asignado a '{nombre_grupo}'")
            except Permission.DoesNotExist:
                print(f"  ERROR: El permiso '{cod_permiso}' no existe. Asegúrate de haber corrido las migraciones.")

    print("\nConfiguracion completada.")
    print("\nInstrucciones para restringir un usuario:")
    print("1. Crea el usuario en el panel de administracion (/admin) o mediante codigo.")
    print("2. NO lo hagas superusuario.")
    print("3. Agregalo SOLO al grupo que desees (ej: 'Acceso EPS').")
    print("4. El usuario solo vera la tarjeta correspondiente en su dashboard.")

if __name__ == "__main__":
    setup_access_control()