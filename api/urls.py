from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'profile', views.ProfileViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'timeline', views.TimelineViewSet)
router.register(r'temoignages', views.TemoignageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('subscribe/', views.subscribe, name='api_subscribe'),
    path('posts/<int:post_id>/comments/', views.add_comment, name='api_add_comment'),
    path('send-message/', views.send_message, name='api_send_message'),
    path('send-newsletter/', views.send_newsletter, name='api_send_newsletter'),
    path('send-announcement/', views.send_announcement, name='api_send_announcement'),
]