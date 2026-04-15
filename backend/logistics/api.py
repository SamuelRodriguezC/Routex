from rest_framework import viewsets, permissions
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


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.AllowAny]
    
    
class ExecutionLogsViewSet(viewsets.ModelViewSet):
    queryset = ExecutionLog.objects.all()
    serializer_class = ExecutionLogSerializer
    permission_classes = [permissions.AllowAny]


