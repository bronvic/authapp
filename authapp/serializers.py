from typing import Any, Dict

from rest_framework import serializers

from authapp.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "parent_username",
            "is_active",
            "first_name",
        ]

    def create(self, validated_data: Dict[str, Any]) -> CustomUser:
        validated_data["is_active"] = False
        return super().create(validated_data)
