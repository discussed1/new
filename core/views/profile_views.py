"""
Views related to user profiles.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q, Sum
from ..models import Profile, Post, Comment, Vote
from ..forms import UserUpdateForm, ProfileUpdateForm


def profile(request, username):
    """
    View a user's profile
    """
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    
    # Get user's posts with vote counts
    posts = Post.objects.filter(author=user)\
        .annotate(vote_score=Count('votes', filter=Q(votes__value=1)) - 
                 Count('votes', filter=Q(votes__value=-1)))\
        .order_by('-created_at')
    
    # Get user's comments
    comments = Comment.objects.filter(author=user).order_by('-created_at')
    
    # Get user's communities
    communities = user.communities.all()
    
    # Get overall karma (upvotes - downvotes across all content)
    post_karma = Vote.objects.filter(post__author=user).aggregate(
        karma=Sum('value', default=0)
    )['karma']
    
    comment_karma = Vote.objects.filter(comment__author=user).aggregate(
        karma=Sum('value', default=0)
    )['karma']
    
    total_karma = (post_karma or 0) + (comment_karma or 0)
    
    context = {
        'profile_user': user,
        'profile': profile,
        'posts': posts,
        'comments': comments,
        'communities': communities,
        'post_karma': post_karma or 0,
        'comment_karma': comment_karma or 0,
        'total_karma': total_karma,
        'title': f'{user.username}\'s Profile',
    }
    
    # Calculate additional context needed for the template
    posts_count = posts.count()
    comments_count = comments.count()
    communities_count = communities.count()
    
    # Get reputation level and progress
    reputation_level = profile.get_reputation_level()
    reputation_progress = profile.get_reputation_progress()
    
    context.update({
        'posts_count': posts_count,
        'comments_count': comments_count,
        'communities_count': communities_count,
        'reputation_level': reputation_level,
        'reputation_progress': reputation_progress,
        'page_type': 'view'
    })
    
    return render(request, 'core/profile/profile_page.html', context)


@login_required
def edit_profile(request):
    """
    Edit user's profile
    """
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile', username=request.user.username)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': user_form,  # Template expects u_form not user_form
        'p_form': profile_form,  # Template expects p_form not profile_form
        'title': 'Edit Profile',
        'page_type': 'edit'
    }
    
    return render(request, 'core/profile/profile_page.html', context)