from django.shortcuts import render, redirect, get_object_or_404
from .models import Job
from .forms import JobForm
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q


def employer_home(request):
    return render(request, "jobs/employer/home.html")

def create_job(request):
    if not request.user.is_authenticated or request.user.role != "company":
        return redirect("landing:home")

    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user
            job.save()

            messages.success(request, "Lowongan berhasil dipublikasikan.")
            return redirect("jobs:my_jobs")
    else:
        form = JobForm()

    return render(request, "jobs/employer/create_job.html", {"form": form})

def my_jobs(request):
    if not request.user.is_authenticated or request.user.role != "company":
        return redirect("landing:home")

    jobs = Job.objects.filter(company=request.user).order_by("-created_at")

    return render(
        request,
        "jobs/employer/my_jobs.html",
        {"jobs": jobs}
    )

def job_detail(request, job_id):
    if not request.user.is_authenticated or request.user.role != "company":
        return redirect("landing:home")

    job = get_object_or_404(Job, id=job_id, company=request.user)

    applications = job.applications.select_related("seeker").order_by("-applied_at")

    return render(
        request,
        "jobs/employer/job_detail.html",
        {
            "job": job,
            "applications": applications
        }
    )


def update_job_status(request, job_id):
    if not request.user.is_authenticated or request.user.role != "company":
        return redirect("landing:home")

    job = get_object_or_404(Job, id=job_id, company=request.user)

    if request.method == "POST":
        status = request.POST.get("status")
        if status in ["active", "inactive"]:
            job.status = status
            job.save()
            messages.success(request, "Status lowongan berhasil diperbarui.")

    return redirect("jobs:job_detail", job_id=job.id)

def job_list(request):
    jobs = Job.objects.filter(status="active").order_by("-created_at")

    query = request.GET.get("q")
    location = request.GET.get("location")

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(tasks__icontains=query) |
            Q(requirements__icontains=query)
        )

    if location:
        jobs = jobs.filter(location=location)

    context = {
        "jobs": jobs,
        "location_choices": Job.LOCATION_CHOICES,
    }

    return render(request, "jobs/seeker/job_list.html", context)

@require_POST
def delete_job(request, job_id):
    if not request.user.is_authenticated or request.user.role != "company":
        return redirect("landing:home")

    job = get_object_or_404(Job, id=job_id, company=request.user)
    job.delete()

    messages.success(request, "Lowongan berhasil dihapus.")
    return redirect("jobs:my_jobs")