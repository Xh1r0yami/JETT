from django.db import models
from django.utils import timezone
import uuid
from accounts.models import CustomUser


class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    company = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="jobs",
        limit_choices_to={"role": "company"},
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True)
    salary = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} – {self.company.full_name}"
