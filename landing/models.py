from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        """Membuat user biasa."""
        if not email:
            raise ValueError("Email wajib diisi")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        """Membuat superuser untuk akses admin."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)  # Superuser langsung aktif tanpa verifikasi

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser harus memiliki is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser harus memiliki is_superuser=True.")

        return self.create_user(email, full_name, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    # Status pengguna
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # Untuk sistem verifikasi email
    email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class EmailVerification(models.Model):
    """Model token verifikasi email"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="verifications")
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Token verifikasi untuk {self.user.email}"
