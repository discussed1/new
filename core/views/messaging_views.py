from postman.views import (
    InboxView as BaseInboxView,
    SentView as BaseSentView,
    ArchivesView as BaseArchivesView,
    TrashView as BaseTrashView,
    WriteView as BaseWriteView,
    ReplyView as BaseReplyView,
    MessageView as BaseMessageView,
)

class InboxView(BaseInboxView):
    """
    Override the inbox view to use our consolidated template
    """
    template_name = 'core/messaging/message_folder.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['folder_type'] = 'inbox'
        return context
    
class SentView(BaseSentView):
    """
    Override the sent view to use our consolidated template
    """
    template_name = 'core/messaging/message_folder.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['folder_type'] = 'sent'
        return context
    
class ArchivesView(BaseArchivesView):
    """
    Override the archives view to use our consolidated template
    """
    template_name = 'core/messaging/message_folder.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['folder_type'] = 'archives'
        return context
    
class TrashView(BaseTrashView):
    """
    Override the trash view to use our consolidated template
    """
    template_name = 'core/messaging/message_folder.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['folder_type'] = 'trash'
        return context
    
class WriteView(BaseWriteView):
    """
    Override the write view to use our consolidated template
    """
    template_name = 'core/messaging/message_folder.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['folder_type'] = 'write'
        return context
    
class ReplyView(BaseReplyView):
    """
    Override the reply view to use our consolidated template
    """
    template_name = 'core/messaging/message_folder.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['folder_type'] = 'reply'
        return context
    
class MessageView(BaseMessageView):
    """
    Override the message view to use our consolidated template
    """
    template_name = 'core/messaging/message_folder.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['folder_type'] = 'view'
        # Ensure message object has a valid pk when used in reply link
        if context.get('message') and not context['message'].pk:
            # If for some reason pk is empty, get it from kwargs
            context['message'].pk = self.kwargs.get('message_id')
        return context