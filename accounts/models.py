from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from django.utils import timezone


# ==========================
# CUSTOM USER MANAGER
# ==========================
class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError("Email wajib diisi")

        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, full_name, password, **extra_fields)


# ==========================
# CUSTOM USER
# ==========================
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("seeker", "Job Seeker"),
        ("company", "Company"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"


# ==========================
# EMAIL VERIFICATION
# ==========================
class EmailVerification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="verifications")
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} Token"


# ==========================
# JOB SEEKER PROFILE
# ==========================
class SeekerProfile(models.Model):
    EDUCATION_CHOICES = (
        ("SMA", "SMA / Sederajat"),
        ("D3", "Diploma (D3)"),
        ("S1", "Sarjana (S1)"),
        ("S2", "Magister (S2)"),
        ("other", "Lainnya"),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="seeker_profile")

    # Nama lengkap readonly → disimpan di CustomUser.full_name
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    education = models.CharField(max_length=20, choices=EDUCATION_CHOICES, blank=True)

    def __str__(self):
        return f"Seeker Profile — {self.user.email}"



# ==========================
# COMPANY PROFILE
# ==========================
class CompanyProfile(models.Model):
    INDUSTRY_CHOICES = (
        ("IT", "Teknologi Informasi"),
        ("finance", "Keuangan"),
        ("manufacturing", "Manufaktur"),
        ("education", "Pendidikan"),
        ("services", "Jasa"),
        ("other", "Lainnya"),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="company_profile")

    # nama perusahaan readonly → dari CustomUser.full_name
    owner_name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    industry = models.CharField(max_length=30, choices=INDUSTRY_CHOICES, blank=True)
    description = models.TextField(blank=True)

    # file upload
    logo = models.ImageField(upload_to="company_logos/", null=True, blank=True)

    def __str__(self):
        return f"Company Profile — {self.user.email}"


# ==========================
# RESET PASSWORD
# ==========================
class PasswordResetToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Reset token for {self.user.email}"

