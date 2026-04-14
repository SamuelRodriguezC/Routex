from django.db import models

# =========================================================
# PRIORITY
# =========================================================
# Define el nivel de importancia de una ruta.
# Se usa para ordenamiento y priorización en ejecución.
#
# En MVP se modela como entidad simple para permitir
# futura escalabilidad (ej: pesos dinámicos o scoring).
class Priority(models.Model):
    priority_name = models.CharField(max_length=55)

    def __str__(self):
        return self.priority_name