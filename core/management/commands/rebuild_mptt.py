from django.core.management.base import BaseCommand
from core.models import Comment
from mptt.exceptions import InvalidMove

class Command(BaseCommand):
    help = 'Rebuild the comment MPTT tree structure'

    def handle(self, *args, **options):
        self.stdout.write('Starting MPTT tree rebuild for Comments')
        
        try:
            # Rebuild the tree structure
            Comment.objects.rebuild()
            
            # Verify tree integrity
            valid = Comment.objects.count() == 0 or Comment.objects.filter(level=0).exists()
            
            if valid:
                self.stdout.write(self.style.SUCCESS('MPTT tree successfully rebuilt!'))
            else:
                self.stdout.write(self.style.ERROR('Tree rebuild completed but verification failed.'))
                
        except InvalidMove as e:
            self.stdout.write(self.style.ERROR(f'Error rebuilding tree: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Unexpected error: {e}'))
