from logistics.models import Route, Status, Priority
from .importers.route_excel_reader import RouteExcelReader
from .importers.route_validator import RouteValidator
from .importers.route_persister import RoutePersister
from .execution_log_service import ExecutionLogService

class RouteImportService:

    @staticmethod
    def import_routes(file):

        rows, total_rows = RouteExcelReader.read(file)

        status_qs = Status.objects.all()
        priority_qs = Priority.objects.all()

        valid_rows = []
        errors_output = []

        # ==========================
        # 1. VALIDACIÓN GLOBAL
        # ==========================
        for index, data in enumerate(rows, start=2):

            result = RouteValidator.validate(data, status_qs, priority_qs)

            if result["errors"]:
                errors_output.append({
                    "row": index,
                    "messages": result["errors"]
                })
            else:
                valid_rows.append(result["clean"])

        # ==========================
        # 2. BLOQUEO SI HAY ERRORES
        # ==========================
        if errors_output:
            return {
                "total_rows": total_rows,
                "valid_rows": len(valid_rows),
                "invalid_rows": len(errors_output),
                "errors": errors_output,
                "message": "Excel inválido. No se guardó ningún registro."
            }

        # ==========================
        # 3. PERSISTENCIA GLOBAL
        # ==========================
        for clean in valid_rows:
            Route.objects.create(**clean)

        return {
            "total_rows": total_rows,
            "valid_rows": len(valid_rows),
            "invalid_rows": 0,
            "errors": [],
            "message": "Importación exitosa"
        }