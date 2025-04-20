from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from watson import search as watson
from core.search_adapters import register_search_adapters

class Command(BaseCommand):
    help = 'Rebuilds the Watson search index with proper adapters'

    def handle(self, *args, **options):
        self.stdout.write('Rebuilding search index...')
        
        # First, register our custom search adapters
        register_search_adapters()
        
        # Then rebuild the index using Watson's built-in command
        call_command('buildwatson')
        
        self.stdout.write(self.style.SUCCESS('Search index rebuilt successfully'))
