#!/usr/bin/env python
import os
import django
import sqlite3
import json
import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'discuss.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Profile, Community, Post, Comment, Vote
from django.db import connection

def convert_datetime(dt_str):
    """Convert SQLite datetime string to Python datetime object"""
    if dt_str is None:
        return None
    try:
        return datetime.datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    except (ValueError, AttributeError):
        return datetime.datetime.now()

def migrate_data():
    """Migrate data from SQLite to PostgreSQL"""
    print("Starting data migration from SQLite to PostgreSQL...")
    
    # Connect to SQLite database
    sqlite_conn = sqlite3.connect('db.sqlite3')
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cursor = sqlite_conn.cursor()
    
    # Migrate Users
    print("Migrating Users...")
    sqlite_cursor.execute("SELECT * FROM auth_user")
    users = sqlite_cursor.fetchall()
    
    for user_data in users:
        if not User.objects.filter(username=user_data['username']).exists():
            user = User(
                id=user_data['id'],
                password=user_data['password'],
                last_login=convert_datetime(user_data['last_login']),
                is_superuser=bool(user_data['is_superuser']),
                username=user_data['username'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                is_staff=bool(user_data['is_staff']),
                is_active=bool(user_data['is_active']),
                date_joined=convert_datetime(user_data['date_joined'])
            )
            user.save()
            print(f"Migrated user: {user.username}")
    
    # Migrate Profiles
    print("Migrating Profiles...")
    sqlite_cursor.execute("SELECT * FROM core_profile")
    profiles = sqlite_cursor.fetchall()
    
    for profile_data in profiles:
        user = User.objects.get(id=profile_data['user_id'])
        if not Profile.objects.filter(user=user).exists():
            try:
                karma = profile_data['karma']
            except IndexError:
                karma = 0  # If karma field doesn't exist in old database
                
            profile = Profile(
                id=profile_data['id'],
                user=user,
                bio=profile_data['bio'],
                karma=karma
            )
            profile.save()
            print(f"Migrated profile for user: {user.username}")
    
    # Migrate Communities
    print("Migrating Communities...")
    sqlite_cursor.execute("SELECT * FROM core_community")
    communities = sqlite_cursor.fetchall()
    
    for community_data in communities:
        if not Community.objects.filter(name=community_data['name']).exists():
            community = Community(
                id=community_data['id'],
                name=community_data['name'],
                description=community_data['description'],
                created_at=convert_datetime(community_data['created_at'])
            )
            community.save()
            print(f"Migrated community: {community.name}")
    
    # Migrate Community Memberships
    print("Migrating Community Memberships...")
    sqlite_cursor.execute("SELECT * FROM core_community_members")
    memberships = sqlite_cursor.fetchall()
    
    for membership_data in memberships:
        community = Community.objects.get(id=membership_data['community_id'])
        user = User.objects.get(id=membership_data['user_id'])
        community.members.add(user)
        print(f"Added user {user.username} to community {community.name}")
    
    # Migrate Posts
    print("Migrating Posts...")
    sqlite_cursor.execute("SELECT * FROM core_post")
    posts = sqlite_cursor.fetchall()
    
    for post_data in posts:
        if not Post.objects.filter(id=post_data['id']).exists():
            author = User.objects.get(id=post_data['author_id'])
            community = Community.objects.get(id=post_data['community_id'])
            post = Post(
                id=post_data['id'],
                title=post_data['title'],
                content=post_data['content'],
                url=post_data['url'],
                post_type=post_data['post_type'],
                created_at=convert_datetime(post_data['created_at']),
                author=author,
                community=community
            )
            post.save()
            print(f"Migrated post: {post.title}")
    
    # Migrate Comments
    print("Migrating Comments...")
    sqlite_cursor.execute("SELECT * FROM core_comment")
    comments = sqlite_cursor.fetchall()
    
    # First pass: create all comments without parent relationships
    comment_map = {}
    for comment_data in comments:
        if not Comment.objects.filter(id=comment_data['id']).exists():
            author = User.objects.get(id=comment_data['author_id'])
            post = Post.objects.get(id=comment_data['post_id'])
            comment = Comment(
                id=comment_data['id'],
                content=comment_data['content'],
                created_at=convert_datetime(comment_data['created_at']),
                author=author,
                post=post,
                parent=None  # Will set parent in second pass
            )
            comment.save()
            comment_map[comment.id] = comment
            print(f"Migrated comment by {author.username}")
    
    # Second pass: set parent relationships
    for comment_data in comments:
        if comment_data['parent_id'] is not None:
            comment = comment_map.get(comment_data['id'])
            parent = comment_map.get(comment_data['parent_id'])
            if comment and parent:
                comment.parent = parent
                comment.save()
                print(f"Set parent for comment {comment.id}")
    
    # Migrate Votes
    print("Migrating Votes...")
    sqlite_cursor.execute("SELECT * FROM core_vote")
    votes = sqlite_cursor.fetchall()
    
    for vote_data in votes:
        user = User.objects.get(id=vote_data['user_id'])
        
        # Check if this is a post vote or comment vote
        post = None
        comment = None
        if vote_data['post_id'] is not None:
            post = Post.objects.get(id=vote_data['post_id'])
        else:
            comment = Comment.objects.get(id=vote_data['comment_id'])
        
        # Skip if vote already exists
        vote_exists = Vote.objects.filter(
            user=user,
            post=post,
            comment=comment
        ).exists()
        
        if not vote_exists:
            vote = Vote(
                id=vote_data['id'],
                user=user,
                post=post,
                comment=comment,
                value=vote_data['value']
            )
            vote.save()
            print(f"Migrated vote by {user.username}")
    
    # Close SQLite connection
    sqlite_conn.close()
    
    print("Data migration completed successfully!")

if __name__ == "__main__":
    migrate_data()