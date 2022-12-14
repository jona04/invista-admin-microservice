from django.core.management import BaseCommand

from core.models import Servico

class Command(BaseCommand):
    def handle(self, *args, **options):
        servicos = Servico.objects.using('old').all()

        for servico in servicos:
            if servico.id > 26534:
                print(servico.id)
                Servico.objects.create(
                    id = servico.id,
                    nome = servico.nome,
                    cliente = servico.cliente,
                    chapa =  servico.chapa,
                    quantidade = servico.quantidade,
                    created_at = servico.created_at,
                    uploaded_at = servico.uploaded_at
                )

