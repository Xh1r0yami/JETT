from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import CustomUser, EmailVerification

def index(request):
    return render(request, "index.html")

def homepage(request):
    return render(request, "homepage.html")

def homepage_kerja(request):
    return render(request, "homepage_kerja.html")

def homepage_staff(request):
    return render(request, "homepage_staff.html")

def logout_user(request):
    logout(request)
    return redirect("index")


def register_user(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        # Validasi dasar
        if not full_name or not email or not password:
            return JsonResponse({"status": "error", "message": "Semua field wajib diisi."})

        if password != confirm_password:
            return JsonResponse({"status": "error", "message": "Password tidak cocok."})

        if len(password) < 6:
            return JsonResponse({"status": "error", "message": "Password minimal 6 karakter."})

        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({"status": "error", "message": "Email sudah digunakan."})

        # Buat user (non-active sampai verifikasi)
        user = CustomUser.objects.create_user(email=email, full_name=full_name, password=password)
        user.is_active = False
        user.save()

        # Buat token verifikasi dan kirim email
        verification = EmailVerification.objects.create(user=user)
        verify_link = request.build_absolute_uri(f"/verify-email/{verification.token}/")

        # Gunakan settings.EMAIL_HOST_USER sebagai from
        from_email = getattr(settings, "EMAIL_HOST_USER", None)
        try:
            send_mail(
                "Verifikasi Akun JETT",
                f"Halo {full_name}, klik link untuk verifikasi:\n{verify_link}",
                from_email,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            # Jika pengiriman email gagal, hapus user & token agar tidak tertinggal
            verification.delete()
            user.delete()
            return JsonResponse({"status": "error", "message": "Gagal mengirim email verifikasi. Cek konfigurasi email."})

        return JsonResponse({"status": "success", "message": "Cek email untuk verifikasi."})

    return JsonResponse({"status": "error", "message": "Request tidak valid."})



def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return JsonResponse({"status": "success"})
            return JsonResponse({"status": "warning", "message": "Akun belum diverifikasi."})

        return JsonResponse({"status": "error", "message": "Email/password salah."})

    return JsonResponse({"status": "error", "message": "Invalid request"})


def verify_email(request, token):
    try:
        verification = EmailVerification.objects.get(token=token)
        user = verification.user
        user.is_active = True
        user.email_verified = True
        user.save()
        verification.delete()

        messages.success(request, "Email berhasil diverifikasi!")
    except:
        messages.error(request, "Token tidak valid.")

    return redirect("index")
