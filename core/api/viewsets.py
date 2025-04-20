from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Profile, Community, Post, Comment, Vote, Notification, Payment
from .serializers import (
    UserSerializer, ProfileSerializer, CommunitySerializer,
    PostListSerializer, PostDetailSerializer, CommentSerializer,
    VoteSerializer, NotificationSerializer, PaymentSerializer
)
from .permissions import IsOwnerOrReadOnly, IsRecipientOrReadOnly, IsAuthorOrReadOnly


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing user information"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']
    
    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        """Get the user's profile"""
        user = self.get_object()
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        """Get the user's posts"""
        user = self.get_object()
        posts = Post.objects.filter(author=user)
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get the user's comments"""
        user = self.get_object()
        comments = Comment.objects.filter(author=user)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class ProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing profile information"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        """Optionally restrict to the current user only"""
        queryset = Profile.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(user__username=username)
        return queryset


class CommunityViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing community information"""
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    
    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        """Get the community's posts"""
        community = self.get_object()
        posts = Post.objects.filter(community=community)
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join the community"""
        community = self.get_object()
        community.members.add(request.user)
        return Response({'status': 'joined community'})
    
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Leave the community"""
        community = self.get_object()
        community.members.remove(request.user)
        return Response({'status': 'left community'})


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing posts"""
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'content', 'author__username', 'community__name']
    filterset_fields = ['post_type', 'community', 'author']
    
    def get_serializer_class(self):
        """Return different serializers for list and detail views"""
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostListSerializer
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get the post's comments"""
        post = self.get_object()
        comments = Comment.objects.filter(post=post, parent=None)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def upvote(self, request, pk=None):
        """Upvote the post"""
        post = self.get_object()
        # Check if user already voted
        try:
            vote = Vote.objects.get(user=request.user, post=post)
            vote.value = 1
            vote.save()
        except Vote.DoesNotExist:
            Vote.objects.create(user=request.user, post=post, value=1)
        return Response({'status': 'post upvoted'})
    
    @action(detail=True, methods=['post'])
    def downvote(self, request, pk=None):
        """Downvote the post"""
        post = self.get_object()
        # Check if user already voted
        try:
            vote = Vote.objects.get(user=request.user, post=post)
            vote.value = -1
            vote.save()
        except Vote.DoesNotExist:
            Vote.objects.create(user=request.user, post=post, value=-1)
        return Response({'status': 'post downvoted'})


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing comments"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'author', 'parent']
    
    @action(detail=True, methods=['get'])
    def replies(self, request, pk=None):
        """Get the comment's replies"""
        comment = self.get_object()
        replies = Comment.objects.filter(parent=comment)
        serializer = CommentSerializer(replies, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def upvote(self, request, pk=None):
        """Upvote the comment"""
        comment = self.get_object()
        # Check if user already voted
        try:
            vote = Vote.objects.get(user=request.user, comment=comment)
            vote.value = 1
            vote.save()
        except Vote.DoesNotExist:
            Vote.objects.create(user=request.user, comment=comment, value=1)
        return Response({'status': 'comment upvoted'})
    
    @action(detail=True, methods=['post'])
    def downvote(self, request, pk=None):
        """Downvote the comment"""
        comment = self.get_object()
        # Check if user already voted
        try:
            vote = Vote.objects.get(user=request.user, comment=comment)
            vote.value = -1
            vote.save()
        except Vote.DoesNotExist:
            Vote.objects.create(user=request.user, comment=comment, value=-1)
        return Response({'status': 'comment downvoted'})


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing notifications"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecipientOrReadOnly]
    
    def get_queryset(self):
        """Return only the current user's notifications"""
        return Notification.objects.filter(recipient=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification marked as read'})
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return Response({'status': 'all notifications marked as read'})


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing payment information"""
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return only the current user's payments"""
        return Payment.objects.filter(user=self.request.user)