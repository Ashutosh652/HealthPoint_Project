"""healthpoint_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from account import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', account_views.register, name='register'),
    path('user_register/', account_views.UserRegister.as_view(), name='user_register'),
    path('doctor_register/', account_views.DoctorRegister.as_view(), name='doctor_register'),
    path('profile/', account_views.profile, name='profile'),
    path('login/', account_views.loginpage, name='login'),
    path('logout/', account_views.logoutpage, name='logout'),
    path('', include('healthpoint.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
