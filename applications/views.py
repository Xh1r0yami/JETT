from django.shortcuts import render, get_object_or_404, redirect
from jobs.models import Job
from .models import JobApplication


def apply_job(request, job_id):
    if not request.user.is_authenticated or request.user.role != "seeker":
        return render(request, "403.html")

    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        JobApplication.objects.create(
            seeker=request.user,
            job=job,
        )
        return redirect("/applications/success/")

    return render(request, "applications/apply.html", {"job": job})


def application_success(request):
    return render(request, "applications/success.html")
