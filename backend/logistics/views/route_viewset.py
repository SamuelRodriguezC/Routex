
from rest_framework import viewsets, permissions
from ..models import Route
from ..serializers import RouteSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from ..services.route_import_service import RouteImportService
from ..services.route_execution_service import RoutesExecutionService
from ..serializers.execution_log_serializer import ExecutionLogSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.AllowAny]

    # Importar rutas desde Excel
    @action(detail=False, methods=["post"], url_path="import")
    def import_routes(self, request):

        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "Debe enviar un archivo Excel"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = RouteImportService.import_routes(file)

        return Response(result, status=status.HTTP_200_OK)
    
    # Ejecutar rutas por IDs
    @action(detail=False, methods=["post"], url_path="execute")
    def execute_routes(self, request):
            route_ids = request.data.get("route_ids", [])

            if not route_ids:
                return Response(
                    {"error": "Debe enviar lista de route_ids"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            result = RoutesExecutionService.execute_routes(route_ids)

            return Response(result, status=status.HTTP_200_OK)
        
    # =====================================================
    # 3 LOGS POR RUTA
    # =====================================================
    @action(detail=True, methods=["get"])
    def logs(self, request, pk=None):
        route = self.get_object()

        logs = route.execution_logs.all().order_by("-execution_time")

        serializer = ExecutionLogSerializer(logs, many=True)

        return Response({
            "route_id": route.id,
            "route": str(route),
            "total_logs": logs.count(),
            "logs": serializer.data
        })