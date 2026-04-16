# routes/services/routes_execution_service.py

from django.db import transaction
from django.utils import timezone

from logistics.models import Route, ExecutionLog


class RoutesExecutionService:

    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    IGNORED = "IGNORED"

    def __init__(self, status_map):
        """
        status_map: dict con IDs o instancias de Status
        Ej:
        {
            "PENDING": status_obj,
            "READY": status_obj,
            "EXECUTED": status_obj,
            "FAILED": status_obj
        }
        """
        self.status_map = status_map

    # -----------------------------
    # VALIDACIÓN SIMULADA
    # -----------------------------
    def _validate_route(self, route: Route):
        if route.distance_km <= 0:
            return False, "Distancia inválida"
        return True, "OK"

    # -----------------------------
    # LOG CENTRALIZADO
    # -----------------------------
    def _log(self, route, result, message):
        ExecutionLog.objects.create(
            route=route,
            result=result,
            message=message
        )

    # -----------------------------
    # EJECUCIÓN POR RUTA
    # -----------------------------
    def process_route(self, route: Route, response_bucket: dict):

        try:
            status = route.status.description.upper()

            # =========================
            # PENDING → READY
            # =========================
            if status == "PENDING":

                is_valid, msg = self._validate_route(route)

                if not is_valid:
                    self._log(route, self.FAILED, msg)
                    response_bucket["failed"].append(route.id)
                    return

                route.status = self.status_map["READY"]
                route.save()

                self._log(route, self.SUCCESS, "Ruta movida a READY")
                response_bucket["executed"].append(route.id)
                return

            # =========================
            # READY → EXECUTED
            # =========================
            if status == "READY":

                route.status = self.status_map["EXECUTED"]
                route.save()

                self._log(route, self.SUCCESS, "Ruta ejecutada correctamente")
                response_bucket["executed"].append(route.id)
                return

            # =========================
            # FAILED → SOLO LOG
            # =========================
            if status == "FAILED":

                self._log(route, self.FAILED, "Ruta en estado FAILED, no se ejecuta")
                response_bucket["failed"].append(route.id)
                return

            # =========================
            # EXECUTED → IGNORADO
            # =========================
            if status == "EXECUTED":

                self._log(route, self.IGNORED, "Intento duplicado de ejecución")
                response_bucket["ignored"].append(route.id)
                return

        except Exception as e:
            self._log(route, self.FAILED, f"Error inesperado: {str(e)}")
            response_bucket["failed"].append(route.id)

    # -----------------------------
    # EJECUCIÓN MASIVA
    # -----------------------------
    @transaction.atomic
    def execute(self, routes_queryset):

        response = {
            "executed": [],
            "failed": [],
            "ignored": [],
            "summary": {
                "success": 0,
                "failed": 0,
                "ignored": 0
            }
        }

        for route in routes_queryset:
            self.process_route(route, response)

        response["summary"]["success"] = len(response["executed"])
        response["summary"]["failed"] = len(response["failed"])
        response["summary"]["ignored"] = len(response["ignored"])

        return response