from logistics.models import ExecutionLog


class ExecutionLogService:

    @staticmethod
    def log(route, result, message):
        return ExecutionLog.objects.create(
            route=route,
            result=result,
            message=message
        )

    @staticmethod
    def log_multiple_errors(route, errors: list):
        logs = [
            ExecutionLog(
                route=route,
                result="FAILED",
                message=error
            )
            for error in errors
        ]
        ExecutionLog.objects.bulk_create(logs)