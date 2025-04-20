import django_filters
from django import forms
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from taggit.models import Tag

from .models import Post, Community

class PostFilter(django_filters.FilterSet):
    """
    Advanced filter for posts with multiple filtering options
    """
    PERIOD_CHOICES = (
        ('', 'All Time'),
        ('today', 'Today'),
        ('week', 'This Week'),
        ('month', 'This Month'),
        ('year', 'This Year'),
    )
    
    SORT_CHOICES = (
        ('recent', 'Most Recent'),
        ('popular', 'Most Popular'),
        ('comments', 'Most Comments'),
        ('oldest', 'Oldest'),
    )
    
    search = django_filters.CharFilter(
        method='filter_search',
        label='Search',
        widget=forms.TextInput(attrs={'placeholder': 'Search posts...', 'class': 'form-control'})
    )
    
    community = django_filters.ModelMultipleChoiceFilter(
        queryset=Community.objects.all(),
        label='Communities',
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )
    
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        label='Tags',
        to_field_name='slug',
        method='filter_tags',
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )
    
    post_type = django_filters.ChoiceFilter(
        choices=Post.POST_TYPE_CHOICES,
        label='Post Type',
        empty_label='All Types',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    period = django_filters.ChoiceFilter(
        choices=PERIOD_CHOICES,
        label='Time Period',
        method='filter_period',
        empty_label=None,
        initial='',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    min_votes = django_filters.NumberFilter(
        method='filter_min_votes',
        label='Minimum Votes',
        initial=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Min votes', 'class': 'form-control'})
    )
    
    sort = django_filters.ChoiceFilter(
        choices=SORT_CHOICES,
        label='Sort By',
        method='filter_sort',
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial='recent'
    )
    
    class Meta:
        model = Post
        fields = ['search', 'community', 'tags', 'post_type', 'period', 'min_votes', 'sort']
    
    def filter_search(self, queryset, name, value):
        """Custom filter to search in title, content, and author username"""
        if not value:
            return queryset
        
        # Search in multiple fields using Q objects
        return queryset.filter(
            Q(title__icontains=value) | 
            Q(content__icontains=value) | 
            Q(author__username__icontains=value) |
            Q(community__name__icontains=value) |
            Q(tags__name__icontains=value)
        ).distinct()
    
    def filter_tags(self, queryset, name, value):
        """Custom filter to filter by multiple tags (AND logic)"""
        if not value:
            return queryset
        
        # Filter posts that have ALL of the selected tags
        for tag in value:
            queryset = queryset.filter(tags=tag)
        
        return queryset
    
    def filter_period(self, queryset, name, value):
        """Custom filter to filter posts by time period"""
        if not value:
            return queryset
        
        now = timezone.now()
        
        if value == 'today':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif value == 'week':
            start_date = now - timedelta(days=7)
        elif value == 'month':
            start_date = now - timedelta(days=30)
        elif value == 'year':
            start_date = now - timedelta(days=365)
        else:
            return queryset
        
        return queryset.filter(created_at__gte=start_date)
    
    def filter_min_votes(self, queryset, name, value):
        """Custom filter to filter posts with minimum vote count"""
        if value is None:
            return queryset
        
        # Annotate with vote count and filter
        return queryset.annotate(
            total_votes=Count('votes__value')
        ).filter(total_votes__gte=value)
    
    def filter_sort(self, queryset, name, value):
        """Custom filter to sort posts by different criteria"""
        if value == 'recent':
            return queryset.order_by('-created_at')
        elif value == 'popular':
            return queryset.annotate(vote_sum=Count('votes__value')).order_by('-vote_sum')
        elif value == 'comments':
            return queryset.annotate(comment_count=Count('comments')).order_by('-comment_count')
        elif value == 'oldest':
            return queryset.order_by('created_at')
        
        # Default sorting
        return queryset.order_by('-created_at')
