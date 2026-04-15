from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .services.route_import_service import RouteImportService
from rest_framework import status
from rest_framework.decorators import action
from .models import Status, Priority, Route, ExecutionLog
from .serializers import ExecutionLogSerializer, StatusSerializer, PrioritySerializer, RouteSerializer

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [permissions.AllowAny]
    
    
class PriorityViewSet(viewsets.ModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer
    permission_classes = [permissions.AllowAny]


# class RouteViewSet(viewsets.ModelViewSet):
#     queryset = Route.objects.all()
#     serializer_class = RouteSerializer
#     permission_classes = [permissions.AllowAny]
    
    
class ExecutionLogsViewSet(viewsets.ModelViewSet):
    queryset = ExecutionLog.objects.all()
    serializer_class = ExecutionLogSerializer
    permission_classes = [permissions.AllowAny]


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.AllowAny]

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