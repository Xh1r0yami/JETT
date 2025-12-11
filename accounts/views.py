from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required  # untuk decorator
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
import uuid

from .models import CustomUser, EmailVerification, SeekerProfile, CompanyProfile, PasswordResetToken
from .forms import RegisterSeekerForm, RegisterCompanyForm, LoginForm


# ===========================================
# REGISTER SEEKER
# ===========================================
def register_seeker(request):
    """
    Fungsi untuk registrasi Job Seeker.
    - Memvalidasi form
    - Menyimpan user baru (inactive) jika valid
    - Membuat token verifikasi email
    - Mengirim email verifikasi
    - Merespons JSON untuk AJAX frontend
    """
    if request.method == "POST":
        form = RegisterSeekerForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.role = "seeker"
                user.is_active = False  # belum aktif sebelum verifikasi
                user.save()

                # Buat token verifikasi email
                token = EmailVerification.objects.create(user=user)
                verify_url = request.build_absolute_uri(f"/accounts/verify/{token.token}/")

                send_mail(
                    subject="Verifikasi Email Akun JETT",
                    message=f"Klik link berikut untuk verifikasi akun:\n{verify_url}",
                    from_email="noreply@jett.com",
                    recipient_list=[user.email],
                    fail_silently=False,
                )

                return JsonResponse({"status": "success"})

            except Exception as e:
                # Kesalahan tak terduga
                return JsonResponse({"status": "error", "errors": {"__all__": [str(e)]}})
        else:
            # Form tidak valid, kirim semua error rapi
            errors = {field: error_list for field, error_list in form.errors.items()}
            return JsonResponse({"status": "error", "errors": errors})
    else:
        form = RegisterSeekerForm()

    return render(request, "accounts/register_seeker.html", {"form": form, "show_verify_modal": False})


# ===========================================
# REGISTER COMPANY
# ===========================================
def register_company(request):
    """
    Fungsi untuk registrasi Company.
    - Mirip register_seeker
    - Menyimpan user baru dengan role 'company'
    """
    if request.method == "POST":
        form = RegisterCompanyForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.role = "company"
                user.is_active = False
                user.save()

                # Buat token verifikasi email
                token = EmailVerification.objects.create(user=user)
                verify_url = request.build_absolute_uri(f"/accounts/verify/{token.token}/")

                send_mail(
                    subject="Verifikasi Email Perusahaan JETT",
                    message=f"Klik link berikut untuk verifikasi akun:\n{verify_url}",
                    from_email="noreply@jett.com",
                    recipient_list=[user.email],
                    fail_silently=False,
                )

                return JsonResponse({"status": "success"})

            except Exception as e:
                return JsonResponse({"status": "error", "errors": {"__all__": [str(e)]}})
        else:
            errors = {field: error_list for field, error_list in form.errors.items()}
            return JsonResponse({"status": "error", "errors": errors})
    else:
        form = RegisterCompanyForm()

    return render(request, "accounts/register_company.html", {"form": form, "show_verify_modal": False})


# ===========================================
# LOGIN SEEKER
# ===========================================
def login_seeker(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)

            if user is None:
                return JsonResponse({"status": "error", "errors": {"__all__": ["Email atau password salah."]}})

            if user.role != "seeker":
                return JsonResponse({"status": "error", "errors": {"__all__": ["Akun ini bukan akun Job Seeker."]}})

            if not user.is_active:
                return JsonResponse({"status": "error", "errors": {"__all__": ["Akun belum diverifikasi."]}})

            login(request, user)
            return JsonResponse({"status": "success", "username": user.full_name})

        # Form validation error
        return JsonResponse({"status": "error", "errors": form.errors})

    return render(request, "accounts/login_seeker.html", {"form": LoginForm()})



# ===========================================
# LOGIN COMPANY
# ===========================================
def login_company(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)

            if user is None:
                return JsonResponse({"status": "error", "errors": {"__all__": ["Email atau password salah."]}})

            if user.role != "company":
                return JsonResponse({"status": "error", "errors": {"__all__": ["Akun ini bukan akun Perusahaan."]}})

            if not user.is_active:
                return JsonResponse({"status": "error", "errors": {"__all__": ["Akun belum diverifikasi."]}})

            login(request, user)
            return JsonResponse({"status": "success", "username": user.full_name})

        return JsonResponse({"status": "error", "errors": form.errors})

    return render(request, "accounts/login_company.html", {"form": LoginForm()})


# ===========================================
# EMAIL VERIFICATION
# ===========================================
def verify_email(request, token):
    verification = get_object_or_404(EmailVerification, token=token)
    user = verification.user

    # Kalau token belum digunakan
    if not verification.is_used:
        user.is_active = True
        user.email_verified = True
        user.save()

        verification.is_used = True
        verification.save()

    # Login otomatis
    if user.is_active:
        login(request, user)

        # Redirect berdasarkan role (pakai field role)
        if user.role == "seeker":
            return redirect("accounts:seeker_profile")

        if user.role == "company":
            return redirect("accounts:company_profile")

    # Fallback
    return redirect("/")


# ===========================================
# PROFIL SEEKER
# ===========================================
@login_required
def seeker_profile(request):
    user = request.user
    if not hasattr(user, "seeker_profile"):
        SeekerProfile.objects.create(user=user)
    seeker_profile = user.seeker_profile

    if request.method == "POST":
        date_of_birth = request.POST.get("date_of_birth")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        education = request.POST.get("education")

        seeker_profile.date_of_birth = date_of_birth or None
        seeker_profile.address = address
        seeker_profile.phone = phone
        seeker_profile.education = education
        seeker_profile.save()

        return redirect("/")  # atau dashboard

    context = {
        "user": user,
        "seeker_profile": seeker_profile,
    }
    return render(request, "accounts/seeker_profile.html", context)


# ===========================================
# PROFIL COMPANY
# ===========================================
@login_required
def company_profile(request):
    user = request.user
    if not hasattr(user, "company_profile"):
        CompanyProfile.objects.create(user=user)
    company_profile = user.company_profile

    if request.method == "POST":
        owner_name = request.POST.get("owner_name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        industry = request.POST.get("industry")
        description = request.POST.get("description")

        company_profile.owner_name = owner_name
        company_profile.address = address
        company_profile.phone = phone
        company_profile.industry = industry
        company_profile.description = description

        if request.FILES.get("logo"):
            company_profile.logo = request.FILES["logo"]

        company_profile.save()
        return redirect("/")  # atau dashboard

    context = {
        "user": user,
        "company_profile": company_profile,
    }
    return render(request, "accounts/company_profile.html", context)


def login_redirect(request):
    """
    Jika user diarahkan ke /accounts/login/:
    - Jika sudah login, arahkan ke profil sesuai role
    - Jika belum login, arahkan ke login sesuai role default
    """
    user = request.user
    if user.is_authenticated:
        # User sudah login, arahkan ke profil sesuai role
        if user.role == "seeker":
            return redirect("accounts:seeker_profile")
        elif user.role == "company":
            return redirect("accounts:company_profile")
        else:
            # fallback, redirect ke homepage
            return redirect("/")
    else:
        # User belum login, default redirect ke login_seeker
        return redirect("accounts:login_seeker")

# ===========================================
# RESET PASSWORD - REQUEST (AJAX)
# ===========================================
def reset_password_request(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "msg": "Email tidak ditemukan."
            })

        # buat token
        reset_token = PasswordResetToken.objects.create(user=user)
        reset_url = request.build_absolute_uri(
            reverse("accounts:reset_password_confirm", args=[str(reset_token.token)])
        )

        # kirim email
        send_mail(
            subject="Reset Password JETT",
            message=f"Klik link berikut untuk reset password:\n{reset_url}",
            from_email="noreply@jett.com",
            recipient_list=[email],
            fail_silently=False,
        )

        return JsonResponse({
            "status": "success",
            "msg": "Link reset sudah dikirim ke email."
        })

    return JsonResponse({
        "status": "error",
        "msg": "Invalid request."
    })



# ===========================================
# RESET PASSWORD - CONFIRM (buka dari email)
# ===========================================
def reset_password_confirm(request, token):
    reset_obj = get_object_or_404(PasswordResetToken, token=token)
    user = reset_obj.user

    if request.method == "POST":
        password = request.POST.get("password")
        confirm = request.POST.get("password2")

        # validasi
        if not password or not confirm:
            return render(request, "accounts/reset_password_confirm.html", {
                "token": token,
                "error": "Mohon isi semua field."
            })

        if password != confirm:
            return render(request, "accounts/reset_password_confirm.html", {
                "token": token,
                "error": "Password tidak sama."
            })

        # update password
        user.password = make_password(password)
        user.save()

        # hapus token agar tidak bisa dipakai lagi
        reset_obj.delete()

        # gunakan PRG pattern
        messages.success(request, "Password berhasil diganti.")
        return HttpResponseRedirect("/")   # <---- FIX PALING PENTING

    return render(request, "accounts/reset_password_confirm.html", {"token": token})



# ===========================================
# LOGOUT
# ===========================================
def logout_user(request):
    """
    Logout user dan redirect ke halaman utama
    """
    logout(request)
    return redirect("/")

@login_required
def delete_account(request):
    user = request.user

    # Hapus profile dahulu agar signal post_delete berjalan
    if hasattr(user, "company_profile"):
        user.company_profile.delete()

    if hasattr(user, "seeker_profile"):
        user.seeker_profile.delete()

    # terakhir hapus user
    user.delete()

    return redirect("/")
