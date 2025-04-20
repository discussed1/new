from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Post
from taggit.models import Tag

class Command(BaseCommand):
    help = 'Adds default tags to all existing users and posts and removes unwanted tags'
    
    def handle(self, *args, **options):
        # Create the 'news' tag if it doesn't exist
        news_tag, created = Tag.objects.get_or_create(name='news', slug='news')
        
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created new tag: 'news'"))
        
        # Process all user profiles - clear all tags and add only "news"
        user_count = 0
        for user in User.objects.all():
            try:
                profile = user.profile
                
                # Get current interests before clearing
                current_interests = list(profile.interests.all())
                self.stdout.write(f"User {user.username} had interests: {', '.join([tag.name for tag in current_interests])}")
                
                # Clear all tags and add only news
                profile.interests.clear()
                profile.interests.add('news')
                
                self.stdout.write(f"User {user.username} now has interests: news")
                user_count += 1
            except Profile.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"No profile for user {user.username}"))
        
        # Process all posts - clear all tags and add only "news"
        post_count = 0
        for post in Post.objects.all():
            # Clear all tags and add only news
            post.tags.clear()
            post.tags.add('news')
            post_count += 1
        
        self.stdout.write(self.style.SUCCESS(f"Processed {user_count} users and {post_count} posts"))
        self.stdout.write(self.style.SUCCESS(f"All users and posts now have only the 'news' tag"))