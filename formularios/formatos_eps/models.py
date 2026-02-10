from django.db import models

class AccesoModulos(models.Model):
    """
    Modelo virtual para definir permisos personalizados de acceso a los módulos del dashboard.
    """
    class Meta:
        managed = False  # No crea tabla en la DB
        permissions = [
            ("ver_eps", "Puede ver el módulo de EPS"),
            ("ver_certificados", "Puede ver el módulo de Certificados Laborales"),
            ("ver_incapacidades", "Puede ver el módulo de Incapacidades"),
        ]