"""
Views related to search functionality.
"""
from django.shortcuts import render, redirect
from django.db.models import Count, Q, F, Sum
from django.utils import timezone
from django.contrib.auth.models import User
import watson
from ..models import Post, Comment, Community
from ..forms import SearchForm


def search(request):
    """
    Basic search view using watson
    """
    query = request.GET.get('q', '')
    search_form = SearchForm(initial={'query': query})
    
    search_results = []
    
    if query:
        # Use Watson to search across multiple models
        search_results = watson.search(query)
    
    context = {
        'search_form': search_form,
        'search_results': search_results,
        'query': query,
        'title': 'Search Results',
        'page_type': 'results'
    }
    
    return render(request, 'core/search/search_page.html', context)


def advanced_search(request):
    """
    Advanced search with filtering options
    """
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'all')
    sort_by = request.GET.get('sort', 'relevance')
    time_range = request.GET.get('time', 'all')
    community_id = request.GET.get('community', '')
    
    search_form = SearchForm(initial={'query': query})
    communities = Community.objects.all()
    
    # Initialize empty search results
    posts = []
    comments = []
    communities_results = []
    users = []
    
    if query:
        # Build the base search query
        if search_type == 'all' or search_type == 'posts':
            posts_query = Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(author__username__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
            
            # Apply community filter if specified
            if community_id:
                posts_query = posts_query.filter(community_id=community_id)
            
            # Apply time range filter if specified
            if time_range == 'day':
                posts_query = posts_query.filter(created_at__gte=timezone.now() - timezone.timedelta(days=1))
            elif time_range == 'week':
                posts_query = posts_query.filter(created_at__gte=timezone.now() - timezone.timedelta(weeks=1))
            elif time_range == 'month':
                posts_query = posts_query.filter(created_at__gte=timezone.now() - timezone.timedelta(days=30))
            elif time_range == 'year':
                posts_query = posts_query.filter(created_at__gte=timezone.now() - timezone.timedelta(days=365))
            
            # Apply sorting
            if sort_by == 'newest':
                posts_query = posts_query.order_by('-created_at')
            elif sort_by == 'oldest':
                posts_query = posts_query.order_by('created_at')
            elif sort_by == 'most_votes':
                posts_query = posts_query.annotate(
                    vote_count=Count('votes', filter=Q(votes__value=1)) - Count('votes', filter=Q(votes__value=-1))
                ).order_by('-vote_count')
            elif sort_by == 'most_comments':
                posts_query = posts_query.annotate(comment_count=Count('comments')).order_by('-comment_count')
            
            posts = posts_query
        
        if search_type == 'all' or search_type == 'comments':
            comments_query = Comment.objects.filter(
                Q(content__icontains=query) |
                Q(author__username__icontains=query)
            ).distinct()
            
            # Apply community filter if specified
            if community_id:
                comments_query = comments_query.filter(post__community_id=community_id)
            
            # Apply time range filter if specified
            if time_range == 'day':
                comments_query = comments_query.filter(created_at__gte=timezone.now() - timezone.timedelta(days=1))
            elif time_range == 'week':
                comments_query = comments_query.filter(created_at__gte=timezone.now() - timezone.timedelta(weeks=1))
            elif time_range == 'month':
                comments_query = comments_query.filter(created_at__gte=timezone.now() - timezone.timedelta(days=30))
            elif time_range == 'year':
                comments_query = comments_query.filter(created_at__gte=timezone.now() - timezone.timedelta(days=365))
            
            # Apply sorting
            if sort_by == 'newest':
                comments_query = comments_query.order_by('-created_at')
            elif sort_by == 'oldest':
                comments_query = comments_query.order_by('created_at')
            elif sort_by == 'most_votes':
                comments_query = comments_query.annotate(
                    vote_count=Count('votes', filter=Q(votes__value=1)) - Count('votes', filter=Q(votes__value=-1))
                ).order_by('-vote_count')
            
            comments = comments_query
        
        if search_type == 'all' or search_type == 'communities':
            communities_query = Community.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
            
            # Apply sorting
            if sort_by == 'newest':
                communities_query = communities_query.order_by('-created_at')
            elif sort_by == 'oldest':
                communities_query = communities_query.order_by('created_at')
            elif sort_by == 'most_members':
                communities_query = communities_query.annotate(member_count=Count('members')).order_by('-member_count')
            
            communities_results = communities_query
        
        if search_type == 'all' or search_type == 'users':
            users_query = User.objects.filter(
                Q(username__icontains=query) |
                Q(profile__bio__icontains=query) |
                Q(profile__display_name__icontains=query)
            ).distinct()
            
            # Apply sorting
            if sort_by == 'newest':
                users_query = users_query.order_by('-date_joined')
            elif sort_by == 'oldest':
                users_query = users_query.order_by('date_joined')
            elif sort_by == 'most_karma':
                users_query = users_query.annotate(
                    post_karma=Sum('post__votes__value', filter=Q(post__votes__value__gt=0), default=0),
                    comment_karma=Sum('comment__votes__value', filter=Q(comment__votes__value__gt=0), default=0)
                ).annotate(
                    total_karma=F('post_karma') + F('comment_karma')
                ).order_by('-total_karma')
            
            users = users_query
    
    context = {
        'search_form': search_form,
        'posts': posts,
        'comments': comments,
        'communities': communities_results,
        'users': users,
        'communities_list': communities,  # For the filter dropdown
        'query': query,
        'search_type': search_type,
        'sort_by': sort_by,
        'time_range': time_range,
        'community_id': community_id,
        'title': 'Advanced Search',
        'page_type': 'advanced'
    }
    
    return render(request, 'core/search/search_page.html', context)