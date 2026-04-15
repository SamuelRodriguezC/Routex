from rest_framework import viewsets, permissions
from logistics.models import Priority
from logistics.serializers import PrioritySerializer

class PriorityViewSet(viewsets.ModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer
    permission_classes = [permissions.AllowAny]