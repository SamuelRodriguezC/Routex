from django.db import models
from .status import Status
from .priority import Priority

# =========================================================
# ROUTE (ENTIDAD PRINCIPAL DEL SISTEMA)
# =========================================================
# Representa una ruta logística completa.
# Es el núcleo del dominio: todo gira alrededor de esta entidad.
#
#  Este modelo soporta:
# - Importación masiva desde Excel
# - Validación de datos inconsistentes
# - Priorización y ejecución
class Route(models.Model):
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)

    #  Distancia en kilómetros
    # Validación: debe ser > 0 (regla de negocio en service layer)
    distance_km = models.DecimalField(max_digits=10, decimal_places=2)

    #  Ventana de tiempo para ejecución logística
    time_window_start = models.DateTimeField()
    time_window_end = models.DateTimeField()

    #  Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # =====================================================
    # RELACIONES (CORE DEL DOMINIO)
    # =====================================================

    #  Estado actual de la ruta (PENDING, VALIDATED, EXECUTED, etc.)
    # PROTECT evita eliminación accidental de catálogos críticos
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name="routes"
    )

    #  Prioridad operativa de la ruta
    priority = models.ForeignKey(
        Priority,
        on_delete=models.PROTECT,
        related_name="routes"
    )

    # class Meta:
        # =================================================
        # REGLA CRÍTICA DE NEGOCIO
        # =================================================
        #  Evita duplicidad exacta de rutas en el sistema
        # Esto protege la integridad de la carga desde Excel.
        # unique_together = (
        #     "origin",
        #     "destination",
        #     "time_window_start",
        #     "time_window_end",
        # )

    def __str__(self):
        return f"{self.origin} → {self.destination}"

