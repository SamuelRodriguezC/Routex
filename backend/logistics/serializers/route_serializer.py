from rest_framework import serializers
from logistics.models import Route
from .status_serializer import StatusSerializer
from .priority_serializer import PrioritySerializer


class RouteSerializer(serializers.ModelSerializer):
    status_detail = StatusSerializer(source="status", read_only=True)
    priority_detail = PrioritySerializer(source="priority", read_only=True)

    class Meta:
        model = Route
        fields = [
            "id",
            "origin",
            "destination",
            "distance_km",
            "time_window_start",
            "time_window_end",
            "status",
            "priority",
            "status_detail",
            "priority_detail",
            "created_at",
            "updated_at",
        ]