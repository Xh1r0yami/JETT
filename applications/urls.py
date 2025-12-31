from django.urls import path
from . import views

app_name = "applications"

urlpatterns = [
    # ===== SEEKER =====
    path("apply/<int:job_id>/", views.apply_job, name="apply_job"),
    path("my/", views.my_applications, name="my_applications"),

    # ===== COMPANY =====
    path(
        "update/<int:application_id>/",
        views.update_application_status,
        name="update_application_status"
    ),

    # ===== SECURE CV DOWNLOAD =====
    path(
        "download-cv/<int:application_id>/",
        views.download_cv,
        name="download_cv"
    ),
]
