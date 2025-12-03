from django.urls import path
from . import views

app_name = "accounts"  # penting supaya reverse bekerja

urlpatterns = [
    # Login
    path("login/", views.login_redirect, name="login_redirect"),  # <-- baru
    path("login/seeker/", views.login_seeker, name="login_seeker"),
    path("login/company/", views.login_company, name="login_company"),

    # Reset Password
    path("reset/request/", views.reset_password_request, name="reset_password_request"),
    path("reset-password/<str:token>/", views.reset_password_confirm, name="reset_password_confirm"),


    # Register
    path("register/seeker/", views.register_seeker, name="register_seeker"),
    path("register/company/", views.register_company, name="register_company"),

    # Verifikasi email
    path("verify/<uuid:token>/", views.verify_email, name="verify_email"),

    # Profil
    path("seeker/profile/", views.seeker_profile, name="seeker_profile"),
    path("company/profile/", views.company_profile, name="company_profile"),

    # Logout
    path("logout/", views.logout_user, name="logout"),
    path("delete/", views.delete_account, name="delete_account"),

]
