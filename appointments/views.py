from rest_framework import viewsets

from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        queryset = Appointment.objects.all()

        professional_id = self.request.query_params.get("professional")

        if professional_id:
            queryset = queryset.filter(professional_id=professional_id)

        return queryset