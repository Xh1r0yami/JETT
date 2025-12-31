import uuid
import os
from django.db import models
from accounts.models import CustomUser
from jobs.models import Job


def cv_upload_path(instance, filename):
    """
    Simpan CV dengan nama acak (UUID)
    Contoh: cvs/3f2c9c9e-8b6a-4a33-a0f1.pdf
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("cvs", filename)


class Application(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    )

    # ===== Relasi utama =====
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    seeker = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    # ===== Data lamaran =====
    cv = models.FileField(
        upload_to=cv_upload_path
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending"
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.seeker.email} - {self.job.title}"
