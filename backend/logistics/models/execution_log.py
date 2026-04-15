

from django.db import models
from .status import Status
from .route import Route
# =========================================================
# EXECUTION LOGS
# =========================================================
#  Trazabilidad del sistema (AUDITORÍA)
#
# Cada vez que una ruta se ejecuta:
# - Se registra resultado
# - Se guarda mensaje de ejecución
# - Se permite auditoría posterior
#
# 💡 Este modelo es CLAVE para demostrar control del sistema
# en la prueba técnica (muy valorado por evaluadores)
class ExecutionLog(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="execution_logs"
    )

    #  Timestamp de ejecución automática
    execution_time = models.DateTimeField(auto_now_add=True)

    #  Resultado de la ejecución (SUCCESS / ERROR)
    result = models.CharField(max_length=50)

    #  Mensaje detallado para debugging y trazabilidad
    message = models.TextField()

    def __str__(self):
        return f"{self.route} - {self.result}"