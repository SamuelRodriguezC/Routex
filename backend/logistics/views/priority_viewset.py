from rest_framework import viewsets, permissions
from ..models import Priority
from ..serializers import PrioritySerializer

class PriorityViewSet(viewsets.ModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer
    permission_classes = [permissions.AllowAny]