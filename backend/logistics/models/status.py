from django.db import models

# =========================================================
# STATUS
# =========================================================
#  Catálogo de estados posibles de una ruta.
# En un sistema real esto podría venir de una tabla maestra
# o incluso un workflow engine.
#
#  Decisión MVP: tabla simple para mantener flexibilidad
# sin sobre-ingeniería.
class Status(models.Model):
    description = models.CharField(max_length=50)

    #  Auditoría básica: cuándo se creó el estado
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


