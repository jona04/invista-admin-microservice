from django.core.management import BaseCommand

from core.models import Nota

class Command(BaseCommand):
    def handle(self, *args, **options):
        notas = Nota.objects.using('old').all()

        for nota in notas:
            Nota.objects.create(
                id = nota.id,
                desconto = nota.desconto,
                created_at = nota.created_at,
                uploaded_at = nota.uploaded_at,
                obs = nota.obs,
                valor_total_nota = nota.valor_total_nota
            )

