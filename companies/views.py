from django.shortcuts import render
from accounts.models import CustomUser
from jobs.models import Job


def company_dashboard(request):
    if not request.user.is_authenticated or request.user.role != "company":
        return render(request, "403.html")

    jobs = Job.objects.filter(company=request.user)
    return render(request, "companies/dashboard.html", {"jobs": jobs})
