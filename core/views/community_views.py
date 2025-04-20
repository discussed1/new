"""
Views related to communities.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from ..models import Community, Post
from ..forms import CommunityForm


def community_list(request):
    """
    List all communities
    """
    communities = Community.objects.annotate(
        member_count=Count('members'),
        post_count=Count('posts')
    ).order_by('-created_at')
    
    return render(request, 'core/community/community_page.html', {
        'communities': communities,
        'title': 'Communities',
        'page_type': 'list'
    })


@login_required
def create_community(request):
    """
    Create a new community
    """
    if request.method == 'POST':
        form = CommunityForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.creator = request.user
            community.save()
            
            # Automatically join the creator to the community
            community.members.add(request.user)
            
            messages.success(request, f'Community "{community.name}" has been created!')
            return redirect('community_detail', pk=community.pk)
    else:
        form = CommunityForm()
    
    return render(request, 'core/community/community_page.html', {
        'form': form,
        'title': 'Create Community',
        'page_type': 'create'
    })


def community_detail(request, pk, template='core/community/community_detail.html', extra_context=None):
    """
    View a community and its posts
    """
    community = get_object_or_404(Community, pk=pk)
    
    # Get posts with vote counts for this community
    posts = Post.objects.filter(community=community)\
        .select_related('author')\
        .prefetch_related('tags')\
        .annotate(vote_score=Count('votes', filter=Q(votes__value=1)) - 
                 Count('votes', filter=Q(votes__value=-1)))\
        .order_by('-created_at')
    
    # Check if user is a member
    is_member = request.user.is_authenticated and community.members.filter(id=request.user.id).exists()
    
    # Prepare context
    context = {
        'community': community,
        'posts': posts,
        'is_member': is_member,
        'member_count': community.members.count(),
        'title': community.name,
    }
    
    # Add any extra context
    if extra_context:
        context.update(extra_context)
    
    return render(request, template, context)


@login_required
def join_community(request, pk):
    """
    Join a community
    """
    community = get_object_or_404(Community, pk=pk)
    
    if not community.members.filter(id=request.user.id).exists():
        community.members.add(request.user)
        messages.success(request, f'You have joined {community.name}!')
    
    return redirect('community_detail', pk=community.pk)


@login_required
def leave_community(request, pk):
    """
    Leave a community
    """
    community = get_object_or_404(Community, pk=pk)
    
    if community.members.filter(id=request.user.id).exists():
        community.members.remove(request.user)
        messages.success(request, f'You have left {community.name}.')
    
    return redirect('community_detail', pk=community.pk)