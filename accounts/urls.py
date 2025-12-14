from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # ======================
    # LOGIN
    # ======================
    path("login/", views.login_redirect, name="login_redirect"),
    path("login/seeker/", views.login_seeker, name="login_seeker"),
    path("login/company/", views.login_company, name="login_company"),

    # ======================
    # REGISTER
    # ======================
    path("register/seeker/", views.register_seeker, name="register_seeker"),
    path("register/company/", views.register_company, name="register_company"),

    # ======================
    # EMAIL VERIFICATION
    # ======================
    path("verify/<uuid:token>/", views.verify_email, name="verify_email"),

    # ======================
    # PROFILE - FORM SETELAH VERIF
    # ======================
    path("seeker/profile-verif/", views.seeker_profile, name="seeker_profile_verif"),
    path("company/profile-verif/", views.company_profile, name="company_profile_verif"),

    # ======================
    # PROFILE - VIEW (READ ONLY)
    # ======================
    path("seeker/profile/", views.seeker_profile_view, name="seeker_profile"),
    path("company/profile/", views.company_profile_view, name="company_profile"),

    # ======================
    # RESET PASSWORD
    # ======================
    path("reset/request/", views.reset_password_request, name="reset_password_request"),
    path("reset-password/<str:token>/", views.reset_password_confirm, name="reset_password_confirm"),

    # ======================
    # LOGOUT / DELETE
    # ======================
    path("logout/", views.logout_user, name="logout"),
    path("delete/", views.delete_account, name="delete_account"),
]
