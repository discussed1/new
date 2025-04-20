from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from payments import urls as payment_urls
from .views.notification_views import notification_list, mark_notification_read, mark_all_notifications_read

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # User profiles
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    
    # Communities
    path('communities/', views.community_list, name='community_list'),
    path('communities/new/', views.create_community, name='create_community'),
    path('communities/<int:pk>/', views.community_detail, name='community_detail'),
    path('communities/<int:pk>/join/', views.join_community, name='join_community'),
    path('communities/<int:pk>/leave/', views.leave_community, name='leave_community'),
    
    # Posts
    path('communities/<int:community_id>/post/text/', views.create_text_post, name='create_text_post'),
    path('communities/<int:community_id>/post/link/', views.create_link_post, name='create_link_post'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/<int:pk>/delete/', views.delete_post, name='delete_post'),
    
    # Comments
    path('posts/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('comments/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('comments/<int:pk>/thread/', views.comment_thread, name='comment_thread'),
    
    # Voting
    path('posts/<int:pk>/vote/<str:vote_type>/', views.vote_post, name='vote_post'),
    path('comments/<int:pk>/vote/<str:vote_type>/', views.vote_comment, name='vote_comment'),
    
    # Search
    path('search/', views.search, name='search'),
    path('advanced-search/', views.advanced_search, name='advanced_search'),
    
    # Notifications
    path('notifications/', notification_list, name='notification_list'),
    path('notifications/mark-read/<int:pk>/', mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', mark_all_notifications_read, name='mark_all_notifications_read'),
    
    # Messaging is handled in main urls.py with namespace='postman'
    # See core.messaging_urls and discuss.urls.py for implementation
    
    # Donations
    path('donate/', views.donate, name='donate'),  # Function name is donate, not donation_view
    path('donate/confirm/', views.donation_confirmation, name='donation_confirmation'),
    path('donate/process/<int:payment_id>/', views.process_payment, name='process_payment'),
    path('donate/success/', views.payment_success, name='payment_success'),
    path('donate/failure/', views.payment_failure, name='payment_failure'),
    path('donate/history/', views.donation_history, name='donation_history'),
    
    # Django Payments URLs
    path('payments/', include(payment_urls)),
    
    # Error testing
    path('sentry-test/', views.sentry_test, name='sentry_test'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
