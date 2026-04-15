from rest_framework import serializers
from logistics.models import ExecutionLog


class ExecutionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutionLog
        fields = "__all__"
        read_only_fields = ('id', 'created_at')