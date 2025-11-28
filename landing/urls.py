from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('homepage/', views.homepage, name='homepage'),
    path('homepage_kerja/', views.homepage_kerja, name='homepage_kerja'),
    path('homepage_staff/', views.homepage_staff, name='homepage_staff'),
    path('register_user/', views.register_user, name='register_user'),
    path('login_user/', views.login_user, name='login_user'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
    path('logout/', views.logout_user, name='logout'),
    
]
