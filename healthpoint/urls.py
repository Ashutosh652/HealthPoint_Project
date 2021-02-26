from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='healthpoint-home'),
    path('about/', views.about, name='healthpoint-about'),
]