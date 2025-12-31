from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import FileResponse, HttpResponseForbidden, Http404
import os

from .models import Application
from .forms import ApplicationForm
from jobs.models import Job


def apply_job(request, job_id):
    if not request.user.is_authenticated or request.user.role != "seeker":
        return redirect("landing:home")

    job = get_object_or_404(Job, id=job_id, status="active")

    # Cegah apply job yang sama 2x
    if Application.objects.filter(job=job, seeker=request.user).exists():
        messages.warning(request, "Kamu sudah melamar pekerjaan ini.")
        return redirect("jobs:job_list")

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.seeker = request.user
            application.save()

            messages.success(request, "Lamaran berhasil dikirim.")
            return redirect("applications:my_applications")
    else:
        form = ApplicationForm()

    return render(
        request,
        "applications/seeker/apply_job.html",
        {
            "form": form,
            "job": job
        }
    )


def my_applications(request):
    if not request.user.is_authenticated or request.user.role != "seeker":
        return redirect("landing:home")

    applications = (
        Application.objects
        .filter(seeker=request.user)
        .select_related("job")
        .order_by("-applied_at")
    )

    return render(
        request,
        "applications/seeker/my_applications.html",
        {"applications": applications}
    )


def download_cv(request, application_id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    application = get_object_or_404(Application, id=application_id)

    # Authorization:
    # - Seeker: hanya CV miliknya
    # - Company: hanya CV untuk job miliknya
    if request.user.role == "seeker":
        if application.seeker != request.user:
            return HttpResponseForbidden()

    elif request.user.role == "company":
        if application.job.company != request.user:
            return HttpResponseForbidden()

    else:
        return HttpResponseForbidden()

    if not application.cv:
        raise Http404("CV tidak ditemukan")

    return FileResponse(
        application.cv.open("rb"),
        as_attachment=True,
        filename="CV.pdf"
    )


def update_application_status(request, application_id):
    if not request.user.is_authenticated or request.user.role != "company":
        return redirect("landing:home")

    application = get_object_or_404(
        Application,
        id=application_id,
        job__company=request.user
    )

    if request.method == "POST":
        status = request.POST.get("status")

        if status in ["accepted", "rejected"]:
            application.status = status
            application.save()

            # ===== EMAIL NOTIFICATION =====
            if status == "accepted":
                subject = "Selamat! Lamaran Anda Diterima 🎉"
                message = f"""
Halo {application.seeker.full_name},

Selamat! 🎉

Lamaran Anda untuk posisi:
{application.job.title}
di perusahaan:
{application.job.company.full_name}

TELAH DITERIMA.

Silakan menunggu informasi lanjutan dari perusahaan.
Semoga sukses!

—
JETT | Job Explore Top Talent
"""
            else:
                subject = "Informasi Lamaran Pekerjaan"
                message = f"""
Halo {application.seeker.full_name},

Terima kasih telah melamar posisi:
{application.job.title}
di perusahaan:
{application.job.company.full_name}

Mohon maaf, saat ini lamaran Anda BELUM DAPAT kami lanjutkan.
Jangan menyerah dan terus mencoba peluang lainnya.

—
JETT | Job Explore Top Talent
"""

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[application.seeker.email],
                fail_silently=True,
            )

    return redirect(
        "jobs:job_detail",
        job_id=application.job.id
    )
