from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.conf import settings


from .models import CustomUser, EmailVerification, SeekerProfile, CompanyProfile, PasswordResetToken
from .forms import RegisterSeekerForm, RegisterCompanyForm, LoginForm


# ===========================================
# REGISTER SEEKER
# ===========================================
def register_seeker(request):
    if request.method == "POST":
        form = RegisterSeekerForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "seeker"
            user.is_active = False
            user.save()

            token = EmailVerification.objects.create(user=user)
            verify_url = request.build_absolute_uri(f"/accounts/verify/{token.token}/")

            send_mail(
                subject="Verifikasi Email Akun JETT",
                message=f"""
Halo {user.full_name},

Terima kasih telah mendaftar sebagai pencari kerja di JETT.

Untuk mengaktifkan akun dan mulai melamar pekerjaan, silakan lakukan verifikasi email melalui tautan berikut:

{verify_url}

Jika pendaftaran ini tidak dilakukan oleh Anda, abaikan email ini.

—
JETT | Job Explore Top Talent
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )

            return JsonResponse({"status": "success"})

        return JsonResponse({"status": "error", "errors": form.errors})

    return render(request, "accounts/register_seeker.html", {"form": RegisterSeekerForm()})


# ===========================================
# REGISTER COMPANY
# ===========================================
def register_company(request):
    if request.method == "POST":
        form = RegisterCompanyForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "company"
            user.is_active = False
            user.save()

            token = EmailVerification.objects.create(user=user)
            verify_url = request.build_absolute_uri(f"/accounts/verify/{token.token}/")

            send_mail(
                subject="Verifikasi Email Perusahaan JETT",
                message=f"""
Halo {user.full_name},

Terima kasih telah mendaftarkan akun perusahaan di platform JETT.

Untuk mengaktifkan akun perusahaan dan mulai mengelola lowongan pekerjaan, silakan lakukan verifikasi email melalui tautan berikut:

{verify_url}

Jika pendaftaran ini tidak dilakukan oleh pihak perusahaan yang bersangkutan, email ini dapat diabaikan.

—
JETT | Job Explore Top Talent
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )

            return JsonResponse({"status": "success"})

        return JsonResponse({"status": "error", "errors": form.errors})

    return render(request, "accounts/register_company.html", {"form": RegisterCompanyForm()})



# ===========================================
# LOGIN SEEKER
# ===========================================
def login_seeker(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )

            if not user or user.role != "seeker" or not user.is_active:
                return JsonResponse({"status": "error"})

            login(request, user)
            return JsonResponse({"status": "success"})

        return JsonResponse({"status": "error", "errors": form.errors})

    return render(request, "accounts/login_seeker.html", {"form": LoginForm()})


# ===========================================
# LOGIN COMPANY
# ===========================================
def login_company(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )

            if not user or user.role != "company" or not user.is_active:
                return JsonResponse({"status": "error"})

            login(request, user)
            return JsonResponse({"status": "success"})

        return JsonResponse({"status": "error", "errors": form.errors})

    return render(request, "accounts/login_company.html", {"form": LoginForm()})


# ===========================================
# EMAIL VERIFICATION
# ===========================================
def verify_email(request, token):
    verification = get_object_or_404(
        EmailVerification,
        token=token,
        is_used=False  # 🔒 HANYA TOKEN YANG BELUM DIPAKAI
    )

    user = verification.user

    # Aktifkan akun
    user.is_active = True
    user.email_verified = True
    user.save()

    # Tandai token sudah dipakai
    verification.is_used = True
    verification.save()

    # Login user
    login(request, user)

    # Redirect sesuai role
    if user.role == "seeker":
        return redirect("accounts:seeker_profile_verif")

    if user.role == "company":
        return redirect("accounts:company_profile_verif")

    return redirect("/")


# ===========================================
# SEEKER PROFILE (FORM SETELAH VERIF)
# ===========================================
@login_required
def seeker_profile(request):
    if request.user.role != "seeker":
        return redirect("/")

    seeker_profile, _ = SeekerProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        seeker_profile.date_of_birth = request.POST.get("date_of_birth") or None
        seeker_profile.address = request.POST.get("address")
        seeker_profile.phone = request.POST.get("phone")
        seeker_profile.education = request.POST.get("education")
        seeker_profile.save()

        # 👉 REDIRECT KE JOB LIST
        return redirect("jobs:job_list")

    return render(request, "accounts/seeker_profile.html", {
        "user": request.user,
        "seeker_profile": seeker_profile
    })


# ===========================================
# SEEKER PROFILE VIEW (READ ONLY)
# ===========================================
@login_required
def seeker_profile_view(request):
    if request.user.role != "seeker":
        return redirect("/")
    seeker_profile, _ = SeekerProfile.objects.get_or_create(user=request.user)

    return render(request, "accounts/seeker_profile_view.html", {
        "user": request.user,
        "seeker_profile": seeker_profile
    })


# ===========================================
# COMPANY PROFILE (FORM SETELAH VERIF)
# ===========================================
@login_required
def company_profile(request):
    if request.user.role != "company":
        return redirect("/")

    company_profile, _ = CompanyProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        company_profile.owner_name = request.POST.get("owner_name")
        company_profile.address = request.POST.get("address")
        company_profile.phone = request.POST.get("phone")
        company_profile.industry = request.POST.get("industry")
        company_profile.description = request.POST.get("description")

        if request.FILES.get("logo"):
            company_profile.logo = request.FILES["logo"]

        company_profile.save()

        # 👉 REDIRECT KE EMPLOYER HOME
        return redirect("jobs:employer_home")

    return render(request, "accounts/company_profile.html", {
        "user": request.user,
        "company_profile": company_profile
    })


# ===========================================
# COMPANY PROFILE VIEW (READ ONLY)
# ===========================================
@login_required
def company_profile_view(request):
    if request.user.role != "company":
        return redirect("/")
    company_profile, _ = CompanyProfile.objects.get_or_create(user=request.user)

    return render(request, "accounts/company_profile_view.html", {
        "user": request.user,
        "company_profile": company_profile
    })


# ===========================================
# LOGIN REDIRECT
# ===========================================
def login_redirect(request):
    if request.user.is_authenticated:
        if request.user.role == "seeker":
            return redirect("accounts:seeker_profile")
        if request.user.role == "company":
            return redirect("accounts:company_profile")
    return redirect("accounts:login_seeker")


# ===========================================
# RESET PASSWORD
# ===========================================
def reset_password_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return JsonResponse({"status": "error"})

        token = PasswordResetToken.objects.create(user=user)
        reset_url = request.build_absolute_uri(
            reverse("accounts:reset_password_confirm", args=[token.token])
        )

        send_mail(
            subject="Permintaan Reset Password Akun JETT",
            message=f"""
Halo {user.full_name},

Kami menerima permintaan untuk melakukan reset password pada akun JETT Anda.

Silakan klik tautan berikut untuk mengatur password baru:

{reset_url}

Jika Anda tidak merasa melakukan permintaan ini, abaikan email ini dan tidak perlu melakukan tindakan apa pun.

—
JETT | Job Explore Top Talent
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error"})



def reset_password_confirm(request, token):
    reset_obj = get_object_or_404(PasswordResetToken, token=token)
    user = reset_obj.user

    if request.method == "POST":
        if request.POST.get("password") != request.POST.get("password2"):
            return render(request, "accounts/reset_password_confirm.html", {"error": "Password tidak sama"})

        user.password = make_password(request.POST.get("password"))
        user.save()
        reset_obj.delete()

        messages.success(request, "Password berhasil diganti.")
        return HttpResponseRedirect("/")

    return render(request, "accounts/reset_password_confirm.html")


# ===========================================
# LOGOUT & DELETE
# ===========================================
def logout_user(request):
    logout(request)
    return redirect("/")


@login_required
def delete_account(request):
    if hasattr(request.user, "company_profile"):
        request.user.company_profile.delete()
    if hasattr(request.user, "seeker_profile"):
        request.user.seeker_profile.delete()

    request.user.delete()
    return redirect("/")
