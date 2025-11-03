from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import CustomUser, EmailVerification

def index(request):
    return render(request, 'index.html')

def homepage(request):
    if not request.user.is_authenticated:
        return redirect('index')
    return render(request, 'homepage.html')

def homepage_kerja(request):
    if not request.user.is_authenticated:
        return redirect('index')
    return render(request, 'homepage_kerja.html')

def homepage_staff(request):
    if not request.user.is_authenticated:
        return redirect('index')
    return render(request, 'homepage_staff.html')

def register_user(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Cek apakah email sudah terdaftar
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email sudah digunakan.'})

        # Buat user baru dengan status belum aktif
        user = CustomUser.objects.create_user(email=email, full_name=full_name, password=password)
        user.is_active = False
        user.save()

        # Buat token verifikasi dan link verifikasi
        verification = EmailVerification.objects.create(user=user)
        verify_link = request.build_absolute_uri(f"/verify-email/{verification.token}/")

        try:
            send_mail(
                subject="Verifikasi Akun JETT",
                message=f"Halo {full_name},\n\nKlik tautan berikut untuk verifikasi akun Anda:\n{verify_link}\n\nTerima kasih telah mendaftar di JETT!",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            return JsonResponse({'status': 'success', 'message': 'Registrasi berhasil! Cek email untuk verifikasi.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Gagal mengirim email: {e}'})

    return JsonResponse({'status': 'error', 'message': 'Metode tidak valid.'})


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return JsonResponse({'status': 'success', 'message': 'Login berhasil!'})
            return JsonResponse({'status': 'warning', 'message': 'Akun belum diverifikasi. Silakan cek email Anda.'})
        return JsonResponse({'status': 'error', 'message': 'Email atau password salah.'})

    return JsonResponse({'status': 'error', 'message': 'Metode tidak valid.'})


def logout_user(request):
    logout(request)
    messages.success(request, "Anda telah logout.")
    return redirect('index')


def verify_email(request, token):
    try:
        verification = EmailVerification.objects.get(token=token)
        user = verification.user
        user.is_active = True
        user.save()
        verification.delete()
        messages.success(request, "Verifikasi berhasil! Silakan login.")
    except EmailVerification.DoesNotExist:
        messages.error(request, "Token tidak valid atau sudah digunakan.")
    return redirect('index')
