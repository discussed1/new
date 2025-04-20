"""
Views related to the notification system.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Notification


def get_unread_notification_count(user):
    """Helper function to get unread notification count for a user"""
    if not user.is_authenticated:
        return 0
    return Notification.objects.filter(recipient=user, is_read=False).count()


@login_required
def notification_list(request):
    """View to display all notifications for the current user"""
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_count = get_unread_notification_count(request.user)
    
    return render(request, 'core/notifications/notifications_list.html', {
        'notifications': notifications,
        'unread_count': unread_count,
        'title': 'Notifications'
    })


@login_required
def mark_notification_read(request, pk):
    """View to mark a notification as read"""
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.is_read = True
    notification.save()
    
    # Check first if post exists, then check comment
    if notification.post:
        return redirect('post_detail', pk=notification.post.id)
    elif notification.comment:
        return redirect('post_detail', pk=notification.comment.post.id)
    
    return redirect('notification_list')


@login_required
def mark_all_notifications_read(request):
    """View to mark all notifications as read"""
    Notification.objects.filter(recipient=request.user).update(is_read=True)
    messages.success(request, 'All notifications marked as read.')
    return redirect('notification_list')