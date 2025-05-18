from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import CustomAuthToken

router = DefaultRouter()
router.register(r'profile', views.ProfileViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'timeline', views.TimelineViewSet)
router.register(r'temoignages', views.TemoignageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # Routes existantes
    path('subscribe/', views.subscribe, name='api_subscribe'),
    path('posts/<int:post_id>/comments/', views.add_comment, name='api_add_comment'),
    path('send-message/', views.send_message, name='api_send_message'),
    path('send-newsletter/', views.send_newsletter, name='api_send_newsletter'),
    path('send-announcement/', views.send_announcement, name='api_send_announcement'),
    
    # Nouvelles routes d'authentification
    path('auth/token/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('auth/change-password/', views.change_password, name='api_change_password'),
    path('auth/user-info/', views.get_user_info, name='api_user_info'),
    
    # Route de suivi des visiteurs
    path('track-visitor/', views.track_visitor, name='api_track_visitor'),
    # Ajouter dans les urlpatterns
path('dashboard-stats/', views.dashboard_stats, name='api_dashboard_stats'),
]