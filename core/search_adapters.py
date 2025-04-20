from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.urls import reverse
from watson import search as watson

from .models import Post, Community, Comment, Profile


class PostSearchAdapter(watson.SearchAdapter):
    def get_title(self, obj):
        return obj.title
    
    def get_description(self, obj):
        if obj.post_type == 'text' and obj.content:
            return obj.content
        elif obj.post_type == 'link' and obj.url:
            return obj.url
        return ""
    
    def get_meta(self, obj):
        # Include additional searchable data
        tags = " ".join([tag.name for tag in obj.tags.all()])
        community = obj.community.name
        author = obj.author.username
        return f"{tags} {community} {author}"
    
    def get_url(self, obj):
        return reverse('post_detail', kwargs={'pk': obj.pk})


class CommunitySearchAdapter(watson.SearchAdapter):
    def get_title(self, obj):
        return f"Community: {obj.name}"
    
    def get_description(self, obj):
        return obj.description
    
    def get_url(self, obj):
        return reverse('community_detail', kwargs={'pk': obj.pk})


class CommentSearchAdapter(watson.SearchAdapter):
    def get_title(self, obj):
        return f"Comment on: {obj.post.title}"
    
    def get_description(self, obj):
        return obj.content
    
    def get_meta(self, obj):
        # Include post title and author in search data
        return f"{obj.post.title} {obj.author.username}"
    
    def get_url(self, obj):
        return reverse('post_detail', kwargs={'pk': obj.post.pk})


class UserSearchAdapter(watson.SearchAdapter):
    def get_title(self, obj):
        return f"User: {obj.username}"
    
    def get_description(self, obj):
        return f"User since {obj.date_joined.strftime('%b %Y')}"
    
    def get_url(self, obj):
        return reverse('profile', kwargs={'username': obj.username})


class ProfileSearchAdapter(watson.SearchAdapter):
    def get_title(self, obj):
        return f"Profile: {obj.user.username}"
    
    def get_description(self, obj):
        return obj.bio or ""
    
    def get_meta(self, obj):
        # Include interests in search
        interests = " ".join([tag.name for tag in obj.interests.all()])
        if obj.display_name:
            return f"{obj.display_name} {interests}"
        return interests
    
    def get_url(self, obj):
        return reverse('profile', kwargs={'username': obj.user.username})


def register_search_adapters():
    """
    Register all search adapters with watson
    """
    # Unregister first to avoid errors if already registered
    try:
        watson.unregister(Post)
    except:
        pass
    
    try:
        watson.unregister(Community)
    except:
        pass
    
    try:
        watson.unregister(Comment)
    except:
        pass
    
    try:
        watson.unregister(User)
    except:
        pass
    
    try:
        watson.unregister(Profile)
    except:
        pass
    
    # Now register with our adapters
    watson.register(Post, PostSearchAdapter)
    watson.register(Community, CommunitySearchAdapter)
    watson.register(Comment, CommentSearchAdapter)
    watson.register(User, UserSearchAdapter)
    watson.register(Profile, ProfileSearchAdapter)
