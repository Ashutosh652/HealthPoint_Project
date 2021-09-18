from django.urls import path
from . import views


urlpatterns = [
    path('', views.home.as_view(), name='healthpoint-home'),
    path('about/', views.about, name='healthpoint-about'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/edit/<int:pk>/', views.PostEditView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>/', views.PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/like/', views.AddLike.as_view(), name='like'),
    path('post/<int:pk>/dislike/', views.AddDislike.as_view(), name='dislike'),
    path('post/<int:post_pk>/comment/edit/<int:pk>/', views.CommentEditView.as_view(), name='comment-edit'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('post/<int:post_pk>/comment/<int:pk>/like/', views.AddCommentLike.as_view(), name='comment-like'),
    path('post/<int:post_pk>/comment/<int:pk>/dislike/', views.AddCommentDislike.as_view(), name='comment-dislike'),
    path('post/<int:post_pk>/comment/<int:pk>/reply/', views.CommentReplyView.as_view(), name='comment-reply'),
    path('search/', views.UserSearchView.as_view(), name='search'),
    path('notification/<int:notification_pk>/post/<int:post_pk>/', views.PostNotification.as_view(), name="post-notification"),
    path('notification/<int:notification_pk>/profile/<int:profile_pk>/', views.FollowNotification.as_view(), name="follow-notification"),
    path('notification/delete/<int:notification_pk>/', views.RemoveNotification.as_view(), name="notification-delete"),
]