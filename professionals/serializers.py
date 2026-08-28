from rest_framework import serializers

from .models import Professional


class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = (
            "id",
            "social_name",
            "profession",
            "address",
            "contact",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )