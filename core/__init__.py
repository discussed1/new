default_app_config = 'core.apps.CoreConfig'

def create_default_tags():
    """
    Create default tags for the application if they don't exist.
    This function is called when the application is ready.
    """
    from taggit.models import Tag
    
    default_tags = [
        'discussion', 'question', 'tech', 'news', 'politics', 
        'sports', 'entertainment', 'science', 'education', 'health',
        'gaming', 'art', 'music', 'food', 'travel'
    ]
    
    for tag_name in default_tags:
        Tag.objects.get_or_create(name=tag_name)

def ready():
    """
    Function called by Django when the application is ready.
    We use this to initialize our default tags and register models with Watson search.
    """
    try:
        # Register search adapters
        from .search_adapters import register_search_adapters
        register_search_adapters()
        
        # Create default tags
        create_default_tags()
    except:
        # This might fail during migrations when the database tables don't exist yet
        # We'll just pass and let it be handled when the app is fully loaded
        pass
