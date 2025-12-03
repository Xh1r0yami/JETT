from django.db import models
from django.utils import timezone
import uuid

from accounts.models import CustomUser
from jobs.models import Job


class JobApplication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    seeker = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="applications",
        limit_choices_to={"role": "seeker"},
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    cv_file = models.FileField(upload_to="cv/", blank=True)
    cover_letter = models.TextField(blank=True)

    applied_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.seeker.full_name} → {self.job.title}"
