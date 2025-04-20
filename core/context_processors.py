from taggit.models import Tag
from django.db.models import Count
from .models import Profile

def notification_count(request):
    """
    Context processor that provides the count of unread notifications for the current user.
    """
    unread_count = 0
    
    if request.user.is_authenticated:
        try:
            # If the user is logged in, query their unread notifications
            unread_count = request.user.notifications.filter(is_read=False).count()
        except Exception as e:
            # If there's any error, default to 0
            unread_count = 0
    
    return {
        'unread_notification_count': unread_count,
    }


def popular_tags(request):
    """
    Add popular tags to the template context for all views
    """
    # Get top tags with usage count
    tags = Tag.objects.annotate(num_times=Count('taggit_taggeditem_items')).order_by('-num_times')[:15]
    
    # If no tags exist or less than 3 tags, add default popular ones
    default_tags = []
    existing_tag_names = [tag.name for tag in tags]
    
    # Default popular tags
    default_tag_names = ['news', 'tech', 'politics']
    
    # Check if any default tags are missing and should be added to the display
    for tag_name in default_tag_names:
        if tag_name not in existing_tag_names:
            # For display purposes only - we'll handle creation in the models
            default_tags.append({
                'name': tag_name,
                'slug': tag_name,
                'num_times': 0
            })
    
    # If we have default tags to add and actual tags are less than 15
    if default_tags and len(tags) < 15:
        # Convert queryset to list if needed
        if not isinstance(tags, list):
            tags = list(tags)
        # Add default tags
        for default_tag in default_tags:
            tags.append(default_tag)
    
    return {
        'all_tags': tags,
        'default_tag_names': default_tag_names,
    }


def user_profile(request):
    """
    Add user profile to the template context for all views
    """
    user_profile = None
    
    if request.user.is_authenticated:
        try:
            # Get or create the user's profile
            user_profile, created = Profile.objects.get_or_create(user=request.user)
        except Exception as e:
            # If there's any error, default to None
            user_profile = None
    
    return {
        'user_profile': user_profile,
    }