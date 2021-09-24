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
    path('doctor_updateprofile/<int:pk>/', views.doctor_updateprofile, name='doctor_updateprofile'),
    path('user_profile/<int:pk>/followers/add/', views.AddFollower.as_view(), name='add-follower'),
    path('user_profile/<int:pk>/followers/remove/', views.RemoveFollower.as_view(), name='remove-follower'),
    path('user_profile/<int:pk>/followers/', views.ListFollowers.as_view(), name='list-followers'),
    path('user_profile/<int:pk>/followings/', views.ListFollowings.as_view(), name='list-followings'),
    path('user_profile/<int:pk>/appointment/', views.BookAppointment.as_view(), name='appointment'),
    path('user_profile/<int:pk>/myrequested/appointments/', views.MyRequestedAppointments.as_view(), name='my-requested-appointments'),
    path('user_profile/<int:pk>/requested-to-me/appointments/', views.AppointmentsRequestedToMe.as_view(), name='appointments-requested-to-me'),
    path('user_profile/<int:user_pk>/appointment-accept/<int:pk>/', views.AcceptAppointment.as_view(), name='appointment-accept'),
    path('user_profile/<int:user_pk>/appointment-reject/<int:pk>/', views.RejectAppointment.as_view(), name='appointment-reject'),
    path('user_profile/<int:pk>/accepted/appointments/', views.AcceptedAppointments.as_view(), name='accepted-appointments'),
    path('user_profile/<int:pk>/rejected/appointments/', views.RejectedAppointments.as_view(), name='rejected-appointments'),
    path('user_profile/<int:pk>/accepted_by_me/appointments/', views.AcceptedAppointmentsByMe.as_view(), name='accepted-appointments-by-me'),
    path('user_profile/<int:pk>/rejected_by_me/appointments/', views.RejectedAppointmentsByMe.as_view(), name='rejected-appointments-by-me'),
    path('user_profile/<int:user_pk>/appointment-delete/<int:pk>/', views.AppointmentDeleteView.as_view(), name='appointment-delete'),
    path('inbox/', views.ListThreads.as_view(), name='inbox'),
    path('inbox/create-thread/', views.CreateThread.as_view(), name='create-thread'),
    path('inbox/<int:pk>/', views.ThreadView.as_view(), name='thread'),
    path('inbox/<int:pk>/create-message/', views.CreateMessage.as_view(), name='create-message'),
]