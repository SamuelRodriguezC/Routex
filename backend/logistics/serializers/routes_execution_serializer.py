# routes/serializers/routes_execution_serializer.py

from rest_framework import serializers

class RoutesExecutionSerializer(serializers.Serializer):
    route_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )