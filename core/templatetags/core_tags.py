from django import template
from django.db.models import Q, Count
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.template.defaultfilters import truncatewords_html as django_truncatewords_html
from core.models import Profile
import os

register = template.Library()

# Class name filter is defined later in this file

# Dictionary access filters
@register.filter
def get_item(dictionary, key):
    """
    Get an item from a dictionary using the key.
    This is useful in templates to access dictionary values by key, since Django 
    templates don't allow dictionary lookups with variables.
    
    Usage:
    {{ dictionary|get_item:key_variable }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key)

@register.filter
def dict_get(dictionary, key):
    """
    Alias for get_item, for backward compatibility with templates.
    
    Usage:
    {{ dictionary|dict_get:key_variable }}
    """
    return get_item(dictionary, key)
    
# Assignment tag version for use with 'as' syntax
@register.simple_tag
def get_dict_item(dictionary, key):
    """
    Get an item from a dictionary using the key, for use with 'as' syntax.
    
    Usage:
    {% get_dict_item dictionary key_variable as value %}
    """
    if dictionary is None:
        return None
    return dictionary.get(key)

@register.simple_tag
def get_unread_notification_count(user):
    """
    Return the count of unread notifications for a user.
    This is a placeholder implementation until a proper notification system is built.
    
    Args:
        user: The user to get notification counts for
        
    Returns:
        int: The number of unread notifications
    """
    if not user or not user.is_authenticated:
        return 0
        
    # For now, return 0 as we don't have a full notification system yet
    # In a real implementation, we would query the notification model
    return 0
    
@register.simple_tag
def unread_message_count(user):
    """
    Return the count of unread messages for a user from django-postman.
    
    Args:
        user: The user to get message counts for
        
    Returns:
        int: The number of unread messages
    """
    if not user or not user.is_authenticated:
        return 0
        
    # Import here to avoid circular imports
    try:
        from postman.models import Message
        return Message.objects.inbox_unread_count(user)
    except ImportError:
        return 0

@register.filter
def class_name(obj):
    """
    Return the class name of an object
    
    Usage:
    {{ object|class_name }}
    
    Example:
    {% if object|class_name == 'User' %}
        <!-- do something -->
    {% endif %}
    """
    return obj.__class__.__name__

@register.filter
def fieldtype(field):
    """
    Return the name of the field's widget class.
    Used for conditional rendering in form templates.
    
    Usage:
    {% if field|fieldtype == 'CheckboxInput' %}
        {# Custom rendering for checkboxes #}
    {% endif %}
    """
    return field.field.widget.__class__.__name__

@register.filter
def is_image(file_value):
    """
    Check if a file is an image based on file extension.
    Used for displaying preview of images in form templates.
    
    Usage:
    {% if field.value|is_image %}
        <img src="{{ field.value.url }}" alt="Preview">
    {% endif %}
    """
    if not file_value:
        return False
    
    try:
        # Get the file extension
        _, ext = os.path.splitext(file_value.name.lower())
        # Check if it's an image extension
        return ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']
    except (AttributeError, ValueError):
        return False

@register.filter
def get_reputation_level(user):
    """
    Get the current reputation level of a user based on their karma.
    
    Usage:
    {{ user|get_reputation_level }}
    """
    if user.is_anonymous:
        return "Guest"
    
    try:
        profile = user.profile
        return profile.get_reputation_level()
    except (Profile.DoesNotExist, AttributeError):
        return "New User"

@register.filter
def get_reputation_progress(user):
    """
    Get the progress to the next reputation level as a percentage.
    
    Usage:
    {{ user|get_reputation_progress }}
    """
    if user.is_anonymous:
        return 0
    
    try:
        profile = user.profile
        return profile.get_reputation_progress()
    except (Profile.DoesNotExist, AttributeError):
        return 0

@register.filter
def or_me(username, user):
    """
    Used in messaging system to replace username with 'me' when the user 
    is the current user.
    
    Usage:
    {{ message.sender|or_me:request.user }}
    """
    if user.username == username or str(user.pk) == username:
        return "me"
    return username

@register.filter
def reputation_badge(user_or_karma):
    """
    Generate an HTML badge for user reputation level.
    Can be given either a user object or a karma integer value.
    
    Usage:
    {{ user|reputation_badge }}
    {{ karma_value|reputation_badge }}
    """
    try:
        # Handle if we're given a karma value directly
        if isinstance(user_or_karma, int):
            karma = user_or_karma
            # Get the reputation level based on karma
            level = "New User"
            if karma >= 10000:
                level = "Legend"
            elif karma >= 5000:
                level = "Community Leader"
            elif karma >= 2500:
                level = "Expert"
            elif karma >= 1000:
                level = "Trusted Contributor"
            elif karma >= 500:
                level = "Established Member"
            elif karma >= 100:
                level = "Regular"
        # Handle user object
        elif hasattr(user_or_karma, 'is_anonymous'):
            if user_or_karma.is_anonymous:
                return ""
            profile = user_or_karma.profile
            level = profile.get_reputation_level()
            karma = profile.karma
        else:
            return ""
        
        # Determine badge style based on karma
        badge_class = "bg-secondary"  # Default badge style
        
        if karma >= 10000:  # Legend
            badge_class = "bg-danger"
        elif karma >= 5000:  # Community Leader
            badge_class = "bg-warning text-dark"
        elif karma >= 2500:  # Expert
            badge_class = "bg-info text-dark"
        elif karma >= 1000:  # Trusted Contributor
            badge_class = "bg-primary"
        elif karma >= 500:   # Established Member
            badge_class = "bg-success"
        elif karma >= 100:   # Regular
            badge_class = "bg-light text-dark"
        
        return mark_safe(f'<span class="badge {badge_class} ms-1">{level}</span>')
    except (Profile.DoesNotExist, AttributeError, TypeError):
        return ""


@register.filter
def truncatewords_html(value, arg):
    """
    Truncate HTML string to the specified number of words.
    This is a wrapper around Django's built-in truncatewords_html filter.
    
    Usage:
    {{ html_content|truncatewords_html:50 }}
    """
    return django_truncatewords_html(value, arg)