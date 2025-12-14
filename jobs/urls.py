from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    # Employer
    path("employer/", views.employer_home, name="employer_home"),
    path("create/", views.create_job, name="create_job"),
    path("my-jobs/", views.my_jobs, name="my_jobs"),
    path("<int:job_id>/", views.job_detail, name="job_detail"),
    path("<int:job_id>/status/", views.update_job_status, name="update_job_status"),
    path("<int:job_id>/delete/", views.delete_job, name="delete_job"),


    # Seeker
    path("", views.job_list, name="job_list"),
]
