from rest_framework import serializers

from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = (
            "id",
            "date",
            "professional",
        )
        read_only_fields = (
            "id",
        )