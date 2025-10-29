from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # tambahkan ini supaya halaman utama diarahkan ke app landing
    path('', include('landing.urls')),
]
