from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    UserViewSet, ProfileViewSet, CommunityViewSet, PostViewSet,
    CommentViewSet, NotificationViewSet, PaymentViewSet
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'communities', CommunityViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    # API endpoints (DRF router includes browsable API)
    path('', include(router.urls)),
]