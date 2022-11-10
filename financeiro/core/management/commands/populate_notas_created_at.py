from django.core.management import BaseCommand

from core.models import Nota

class Command(BaseCommand):
    def handle(self, *args, **options):
        notas_old = Nota.objects.using('old').all().order_by('id')[9150:]
    
        for nota_old in notas_old:
            print(nota_old.id)
            nota = Nota.objects.get(pk=nota_old.id)
            nota.created_at = nota_old.created_at
            nota.save()
    