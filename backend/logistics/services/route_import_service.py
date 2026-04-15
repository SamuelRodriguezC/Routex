# logistics/services/route_import_service.py

import openpyxl
from decimal import Decimal
from django.db import transaction
from django.utils.dateparse import parse_datetime
from logistics.models import Route, Status, Priority


class RouteImportService:

    REQUIRED_FIELDS = [
        "origin",
        "destination",
        "distance_km",
        "priority",
        "time_window_start",
        "time_window_end",
        "status",
    ]

    VALID_STATUSES = {"READY", "FAILED", "PENDING", "EXECUTED"}

    @staticmethod
    def import_routes(file):

        workbook = openpyxl.load_workbook(file)
        sheet = workbook.active

        headers = [cell.value for cell in sheet[1]]

        errors = []
        valid_routes = []

        for row_index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):

            data = dict(zip(headers, row))
            row_errors = []

            # ----------------------------
            # 1. Validar campos obligatorios
            # ----------------------------
            for field in RouteImportService.REQUIRED_FIELDS:
                if not data.get(field):
                    row_errors.append(f"{field} es obligatorio")

            if row_errors:
                errors.append({"row": row_index, "errors": row_errors})
                continue

            # ----------------------------
            # 2️. Validaciones de negocio
            # ----------------------------
            origin = str(data["origin"]).strip()
            destination = str(data["destination"]).strip()

            if not origin:
                row_errors.append("origin no puede estar vacío")

            if not destination:
                row_errors.append("destination no puede estar vacío")

            # distance
            try:
                distance = Decimal(data["distance_km"])
                if distance <= 0:
                    row_errors.append("distance_km debe ser mayor que 0")
            except:
                row_errors.append("distance_km debe ser numérico válido")

            # fechas
            start = parse_datetime(str(data["time_window_start"]))
            end = parse_datetime(str(data["time_window_end"]))

            if not start or not end:
                row_errors.append("Formato fecha inválido")
            elif start >= end:
                row_errors.append("time_window_start debe ser menor que time_window_end")

            # ----------------------------
            # 3️. Validar Status (texto → FK)
            # ----------------------------
            status_text = str(data["status"]).strip().upper()

            if status_text not in RouteImportService.VALID_STATUSES:
                row_errors.append("status inválido")

            status_obj = Status.objects.filter(description__iexact=status_text).first()
            if not status_obj:
                row_errors.append("status no existe en base de datos")

            # ----------------------------
            # 4️. Validar Priority FK
            # ----------------------------
            priority_id = data["priority"]

            priority_obj = Priority.objects.filter(id=priority_id).first()
            if not priority_obj:
                row_errors.append("priority no existe")

            # ----------------------------
            # 5️. Validar duplicidad exacta
            # ----------------------------
            if start and end:
                exists = Route.objects.filter(
                    origin=origin,
                    destination=destination,
                    time_window_start=start,
                    time_window_end=end,
                ).exists()

                if exists:
                    row_errors.append("Ruta duplicada (origin + destination + ventana)")

            if row_errors:
                errors.append({"row": row_index, "errors": row_errors})
                continue

            valid_routes.append(
                Route(
                    origin=origin,
                    destination=destination,
                    distance_km=distance,
                    time_window_start=start,
                    time_window_end=end,
                    status=status_obj,
                    priority=priority_obj,
                )
            )

        # ----------------------------
        # 6️. Insert masivo
        # ----------------------------
        if not errors:
            with transaction.atomic():
                Route.objects.bulk_create(valid_routes, batch_size=1000)

        return {
            "total_rows": sheet.max_row - 1,
            "inserted": len(valid_routes) if not errors else 0,
            "errors": errors,
        }