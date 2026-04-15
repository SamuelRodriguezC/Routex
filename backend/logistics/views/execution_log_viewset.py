from rest_framework import viewsets, permissions
from ..models import ExecutionLog
from ..serializers import ExecutionLogSerializer



class ExecutionLogsViewSet(viewsets.ModelViewSet):
    queryset = ExecutionLog.objects.all()
    serializer_class = ExecutionLogSerializer
    permission_classes = [permissions.AllowAny]