from django.db import transaction
from logistics.models import Route

class RoutePersister:

    @staticmethod
    def save(validated_data, status_failed, execution_log_service, row_errors=None):

        with transaction.atomic():

            route = validated_data

            if row_errors:
                route_obj = Route.objects.create(
                    origin=route["origin"] or "INVALID",
                    destination=route["destination"] or "INVALID",
                    distance_km=route["distance_km"],
                    time_window_start=route["time_window_start"],
                    time_window_end=route["time_window_end"],
                    status=status_failed,
                    priority=route["priority"],
                )

                execution_log_service.log_multiple_errors(route_obj, row_errors)

                return route_obj, "FAILED"

            route_obj = Route.objects.create(**route)

            execution_log_service.log(
                route_obj,
                result="SUCCESS",
                message="Ruta importada correctamente"
            )

            return route_obj, "SUCCESS"