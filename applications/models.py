from django.db import models
from accounts.models import CustomUser
from jobs.models import Job

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
        upload_to="cvs/"
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
