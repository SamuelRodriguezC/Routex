from django.db import transaction
from logistics.models import Route, ExecutionLog, Status


class RouteExecutionService:

    @staticmethod
    def execute_routes(route_ids):
        executed_status = Status.objects.get(description="EXECUTED")

        results = {
            "executed": [],
            "skipped": [],
            "errors": []
        }

        with transaction.atomic():
            routes = Route.objects.select_related("status").filter(id__in=route_ids)

            for route in routes:

                current_status = route.status.description.upper()

                # REGLAS DE NEGOCIO
                if current_status == "FAILED":
                    results["skipped"].append({
                        "id": route.id,
                        "reason": "Route is FAILED and cannot be executed"
                    })
                    continue

                if current_status == "EXECUTED":
                    results["skipped"].append({
                        "id": route.id,
                        "reason": "Route already executed"
                    })
                    continue

                if current_status not in ["READY", "PENDING"]:
                    results["skipped"].append({
                        "id": route.id,
                        "reason": f"Invalid status: {current_status}"
                    })
                    continue

                try:
                    route.status = executed_status
                    route.save()

                    ExecutionLog.objects.create(
                        route=route,
                        result="SUCCESS",
                        message="Route executed successfully"
                    )

                    results["executed"].append(route.id)

                except Exception as e:
                    ExecutionLog.objects.create(
                        route=route,
                        result="ERROR",
                        message=str(e)
                    )

                    results["errors"].append({
                        "id": route.id,
                        "error": str(e)
                    })

        return results