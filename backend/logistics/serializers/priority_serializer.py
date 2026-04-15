from rest_framework import serializers
from logistics.models import Priority


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = "__all__"
        read_only_fields = ('id', 'created_at')