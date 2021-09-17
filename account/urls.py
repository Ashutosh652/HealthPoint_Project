from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_register/', views.UserRegister.as_view(), name='user_register'),
    path('doctor_register/', views.DoctorRegister.as_view(), name='doctor_register'),
    path('user_profile/<int:pk>/', login_required(views.UserProfileView.as_view()), name='user_profile'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutpage, name='logout'),
    path('user_updateprofile/<int:pk>/', views.user_updateprofile, name='user_updateprofile'),
    path('doctor_updateprofile/', views.doctor_updateprofile, name='doctor_updateprofile'),
    path('user_profile/<int:pk>/followers/add/', views.AddFollower.as_view(), name='add-follower'),
    path('user_profile/<int:pk>/followers/remove/', views.RemoveFollower.as_view(), name='remove-follower'),
    path('user_profile/<int:pk>/followers/', views.ListFollowers.as_view(), name='list-followers'),
    path('user_profile/<int:pk>/followings/', views.ListFollowings.as_view(), name='list-followings'),
]