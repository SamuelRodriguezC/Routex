from rest_framework import serializers
from logistics.models import Status


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"
        read_only_fields = ('id', 'created_at')