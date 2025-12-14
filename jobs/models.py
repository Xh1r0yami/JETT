from django.db import models
from accounts.models import CustomUser

class Job(models.Model):

    JOB_TYPE_CHOICES = (
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("internship", "Internship"),
        ("freelance", "Freelance"),
    )

    LOCATION_CHOICES = (
        ("jakarta", "Jakarta"),
        ("bogor", "Bogor"),
        ("batam", "Batam"),
        ("tangerang", "Tangerang"),
        ("bandung", "Bandung"),
    )

    SALARY_RANGE_CHOICES = (
        ("3-5", "3–5 juta"),
        ("5-8", "5–8 juta"),
        ("8-12", "8–12 juta"),
        ("12-20", "12–20 juta"),
        ("negotiable", "Negotiable"),
    )

    STATUS_CHOICES = (
        ("active", "Aktif"),
        ("inactive", "Tidak Aktif"),
    )

    # ===== Field sesuai form =====
    title = models.CharField(max_length=200)
    tasks = models.TextField()
    requirements = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES)
    salary_range = models.CharField(max_length=20, choices=SALARY_RANGE_CHOICES)

    # ===== System =====
    company = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="jobs"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="active"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
