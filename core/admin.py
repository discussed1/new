from django.contrib import admin
from .models import Profile, Community, Post, Comment, Vote, Payment

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'bio')

class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'community', 'author', 'created_at', 'post_type')
    list_filter = ('community', 'created_at', 'post_type')
    search_fields = ('title', 'content', 'author__username', 'community__name')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username')

class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'comment', 'value')
    list_filter = ('value',)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'donation_type', 'status', 'created_at', 'total')
    list_filter = ('status', 'donation_type', 'created_at')
    search_fields = ('user__username', 'description')
    readonly_fields = ('token', 'variant', 'status', 'transaction_id', 'currency', 'total', 'delivery', 'tax')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Community, CommunityAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Payment, PaymentAdmin)
