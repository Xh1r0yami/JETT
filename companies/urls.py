from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.company_dashboard, name="company_dashboard"),
]
