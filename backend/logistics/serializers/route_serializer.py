from rest_framework import serializers
from logistics.models import Route, Status, Priority
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
        read_only_fields = ("id", "created_at", "updated_at")

    # =====================================================
    # VALIDACIONES INDIVIDUALES
    # =====================================================

    def validate_origin(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Origin no puede estar vacío")
        return value.strip()

    def validate_destination(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Destination no puede estar vacío")
        return value.strip()

    def validate_distance_km(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("Distance debe ser mayor a 0")
        return value

    def validate_status(self, value):
        if not Status.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Estado inválido")
        return value

    def validate_priority(self, value):
        if value is None or value.id <= 0:
            raise serializers.ValidationError("Invalid priority")
        return value

    # =====================================================
    # VALIDACIÓN CRUZADA (NEGOCIO)
    # =====================================================

    def validate(self, data):
        start = data.get("time_window_start")
        end = data.get("time_window_end")

        if start and end and start >= end:
            raise serializers.ValidationError(
                "time_window_start debe ser anterior a time_window_end"
            )

        if Route.objects.filter(
            origin=data.get("origin"),
            destination=data.get("destination"),
            time_window_start=start,
            time_window_end=end,
        ).exists():
            raise serializers.ValidationError(
                "Duplicate route detected (origin, destination, time window)"
            )

        return data