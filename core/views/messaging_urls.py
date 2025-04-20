from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import pgettext_lazy
from core.views.messaging_views import (
    InboxView, SentView, ArchivesView, TrashView,
    WriteView, ReplyView, MessageView
)
from postman.views import (
    ConversationView, ArchiveView, DeleteView, UndeleteView,
    MarkReadView, MarkUnreadView, IndexView
)

app_name = 'postman'
urlpatterns = [
    # Use re_path with optional 'm' parameter to maintain compatibility with original postman URLs
    re_path(r'^inbox/(?:(?P<option>m)/)?$', InboxView.as_view(), name='inbox'),
    re_path(r'^sent/(?:(?P<option>m)/)?$', SentView.as_view(), name='sent'),
    re_path(r'^archives/(?:(?P<option>m)/)?$', ArchivesView.as_view(), name='archives'),
    re_path(r'^trash/(?:(?P<option>m)/)?$', TrashView.as_view(), name='trash'),
    re_path(r'^write/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(), name='write'),
    re_path(r'^reply/(?P<message_id>[\d]+)/$', ReplyView.as_view(), name='reply'),
    re_path(r'^view/(?P<message_id>[\d]+)/$', MessageView.as_view(), name='view'),
    
    # Keep the original action views
    path('view/t/<int:thread_id>/', ConversationView.as_view(), name='view_conversation'),
    path('archive/', csrf_exempt(ArchiveView.as_view()), name='archive'),
    path('delete/', csrf_exempt(DeleteView.as_view()), name='delete'),
    path('undelete/', csrf_exempt(UndeleteView.as_view()), name='undelete'),
    path('mark-read/', MarkReadView.as_view(), name='mark-read'),
    path('mark-unread/', MarkUnreadView.as_view(), name='mark-unread'),
    path('', IndexView.as_view()),
]