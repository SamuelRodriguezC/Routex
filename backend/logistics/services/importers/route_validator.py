from decimal import Decimal, InvalidOperation
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.db.models import Q

from logistics.models import Route


class RouteValidator:

    REQUIRED_FIELDS = [
        "origin",
        "destination",
        "distance_km",
        "priority",
        "time_window_start",
        "time_window_end",
        "status",
    ]

    @staticmethod
    def parse_datetime(value):
        if not value:
            return None

        dt = parse_datetime(str(value))

        if dt and timezone.is_naive(dt):
            dt = timezone.make_aware(dt)

        return dt

    @staticmethod
    def validate(data, status_queryset, priority_queryset):
        errors = []

        # -----------------------------------------------------
        # LIMPIEZA BÁSICA
        # -----------------------------------------------------
        origin = str(data.get("origin", "")).strip()
        destination = str(data.get("destination", "")).strip()

        # -----------------------------------------------------
        # CAMPOS OBLIGATORIOS
        # -----------------------------------------------------
        for field in RouteValidator.REQUIRED_FIELDS:
            if not data.get(field):
                errors.append(f"{field} es obligatorio")

        # -----------------------------------------------------
        # DISTANCIA
        # -----------------------------------------------------
        distance = None
        try:
            distance = Decimal(str(data.get("distance_km")))
            if distance <= 0:
                errors.append("distance_km debe ser mayor que 0")
        except (InvalidOperation, TypeError):
            errors.append("distance_km inválido")

        # -----------------------------------------------------
        # FECHAS
        # -----------------------------------------------------
        start = RouteValidator.parse_datetime(data.get("time_window_start"))
        end = RouteValidator.parse_datetime(data.get("time_window_end"))

        if not start or not end:
            errors.append("Formato de fecha inválido en ventana de tiempo")
        elif start >= end:
            errors.append("La ventana de tiempo es inválida (inicio mayor que fin)")

        # -----------------------------------------------------
        # STATUS
        # -----------------------------------------------------
        status = status_queryset.filter(
            description__iexact=str(data.get("status", "")).strip()
        ).first()

        if not status:
            errors.append("status no existe")

        # -----------------------------------------------------
        # PRIORITY
        # -----------------------------------------------------
        priority = priority_queryset.filter(
            id=data.get("priority")
        ).first()

        if not priority:
            errors.append("priority no existe")

        # -----------------------------------------------------
        # DUPLICIDAD EN BASE DE DATOS
        # -----------------------------------------------------
        if start and end and origin and destination:
            exists = Route.objects.filter(
                origin__iexact=origin,
                destination__iexact=destination,
                time_window_start=start,
                time_window_end=end
            ).exists()

            if exists:
                errors.append(
                    "Ya existe una ruta con el mismo origen, destino y ventana de tiempo"
                )

        # -----------------------------------------------------
        # RESULTADO FINAL
        # -----------------------------------------------------
        return {
            "errors": errors,
            "clean": {
                "origin": origin,
                "destination": destination,
                "distance_km": distance,
                "time_window_start": start,
                "time_window_end": end,
                "status": status,
                "priority": priority,
            }
        }