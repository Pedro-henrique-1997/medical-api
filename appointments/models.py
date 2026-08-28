import uuid

from django.db import models

from professionals.models import Professional


class Appointment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    date = models.DateTimeField()
    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE,
        related_name="appointments",
    )

    def __str__(self):
        return f"{self.professional.social_name} - {self.date}"