import uuid

from django.db import models


class Professional(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    social_name = models.CharField(max_length=150)
    profession = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.social_name