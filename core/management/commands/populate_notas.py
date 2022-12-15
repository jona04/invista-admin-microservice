from django.core.management import BaseCommand

from core.models import Nota

class Command(BaseCommand):
    def handle(self, *args, **options):
        notas = Nota.objects.using('old').all().order_by('id')
        
        for nota in notas:
            if nota.id > 16517:
                print(nota.id)
                Nota.objects.create(
                    id = nota.id,
                    desconto = nota.desconto,
                    created_at = nota.created_at,
                    uploaded_at = nota.uploaded_at,
                    obs = nota.obs
                )

