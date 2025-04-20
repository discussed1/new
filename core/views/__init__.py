"""
Core views module that imports from functional view modules.
This maintains backward compatibility with existing imports.
"""

# Home view
from .post_views import home

# Profile views
from .profile_views import profile, edit_profile

# Community views
from .community_views import (
    community_list, community_detail, create_community,
    join_community, leave_community
)

# Post views
from .post_views import (
    post_detail, create_text_post, create_link_post,
    delete_post, add_comment, comment_thread,
    delete_comment, vote_post, vote_comment,
    post_votes_api, comment_votes_api,
    get_comment_children
)

# Notification views
from .notification_views import (
    notification_list, mark_notification_read,
    mark_all_notifications_read, get_unread_notification_count
)

# Search views
from .search_views import search, advanced_search

# Payment views
from .payment_views import (
    donate, donation_confirmation, 
    payment_success, payment_failure,
    process_payment, donation_history
)

# Utility views
from .utils_views import sentry_status, sentry_test