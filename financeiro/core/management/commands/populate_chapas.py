from django.core.management import BaseCommand

from core.models import Chapa

class Command(BaseCommand):
    def handle(self, *args, **options):
        chapas = Chapa.objects.using('old').all()

        for chapa in chapas:
            Chapa.objects.create(
                id = chapa.id,
                nome = chapa.nome,
                valor = chapa.valor,
                estoque = chapa.estoque,
                marca = chapa.marca,
                obs = chapa.obs,
                created_at = chapa.created_at,
                uploaded_at = chapa.uploaded_at
            )

