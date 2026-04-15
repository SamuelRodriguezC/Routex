from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .services.route_import_service import RouteImportService
from rest_framework import status
from rest_framework.decorators import action
from .models import Status, Priority, Route, ExecutionLog
from .serializers import ExecutionLogSerializer, StatusSerializer, PrioritySerializer, RouteSerializer

    



# class RouteViewSet(viewsets.ModelViewSet):
#     queryset = Route.objects.all()
#     serializer_class = RouteSerializer
#     permission_classes = [permissions.AllowAny]
    
    


