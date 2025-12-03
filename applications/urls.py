from django.urls import path
from . import views

urlpatterns = [
    path("apply/<uuid:job_id>/", views.apply_job, name="apply_job"),
    path("success/", views.application_success, name="application_success"),
]
