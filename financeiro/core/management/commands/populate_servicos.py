from django.core.management import BaseCommand

from core.models import Servico

class Command(BaseCommand):
    def handle(self, *args, **options):
        servicos = Servico.objects.using('old').all()

        for servico in servicos:
            Servico.objects.create(
                id = servico.id,
                nome = servico.nome,
                cliente = servico.cliente,
                chapa =  servico.chapa,
                quantidade = servico.quantidade,
                created_at = servico.created_at,
                uploaded_at = servico.uploaded_at,
                valor_total_servico = servico.valor_total_servico
            )

