from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import Profile, Community, Post, Comment, Vote, Notification, Payment
from taggit.serializers import TagListSerializerField, TaggitSerializer


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'last_login']


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the Profile model"""
    user = UserSerializer(read_only=True)
    interests = TagListSerializerField()
    reputation_level = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = ['user', 'bio', 'karma', 'country', 'website', 'avatar', 
                  'display_name', 'interests', 'reputation_level']
    
    def get_reputation_level(self, obj):
        return obj.get_reputation_level()


class CommunitySerializer(serializers.ModelSerializer):
    """Serializer for the Community model"""
    member_count = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'created_at', 'member_count', 'post_count']
    
    def get_member_count(self, obj):
        return obj.members.count()
    
    def get_post_count(self, obj):
        return obj.posts.count()


class PostListSerializer(TaggitSerializer, serializers.ModelSerializer):
    """Serializer for list view of Post model"""
    author = UserSerializer(read_only=True)
    community = CommunitySerializer(read_only=True)
    tags = TagListSerializerField()
    vote_score = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'post_type', 'created_at', 'author', 
                  'community', 'tags', 'vote_score', 'comment_count']
    
    def get_vote_score(self, obj):
        return obj.vote_count()
    
    def get_comment_count(self, obj):
        return obj.comment_count()


class PostDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    """Serializer for detail view of Post model"""
    author = UserSerializer(read_only=True)
    community = CommunitySerializer(read_only=True)
    tags = TagListSerializerField()
    vote_score = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'url', 'post_type', 'created_at', 
                  'author', 'community', 'tags', 'vote_score', 'comment_count']
    
    def get_vote_score(self, obj):
        return obj.vote_count()
    
    def get_comment_count(self, obj):
        return obj.comment_count()


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model"""
    author = UserSerializer(read_only=True)
    vote_score = serializers.SerializerMethodField()
    post_id = serializers.PrimaryKeyRelatedField(source='post', read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(source='parent', read_only=True, allow_null=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'author', 'post_id', 
                  'parent_id', 'vote_score']
    
    def get_vote_score(self, obj):
        return obj.vote_count()


class VoteSerializer(serializers.ModelSerializer):
    """Serializer for the Vote model"""
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    
    class Meta:
        model = Vote
        fields = ['id', 'user', 'post', 'comment', 'value', 'created_at']
        

class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for the Notification model"""
    recipient = serializers.SlugRelatedField(read_only=True, slug_field='username')
    sender = serializers.SlugRelatedField(read_only=True, slug_field='username')
    
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'sender', 'notification_type', 
                  'post', 'comment', 'text', 'created_at', 'is_read']


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for the Payment model"""
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    
    class Meta:
        model = Payment
        fields = ['id', 'user', 'donation_type', 'description', 'created_at', 
                  'amount', 'variant', 'status', 'transaction_id']