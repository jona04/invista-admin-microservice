from django.core.management import BaseCommand

from core.models import Servico, Chapa

class Command(BaseCommand):
    def handle(self, *args, **options):
        servicos = Servico.objects.all()

        for servico in servicos:
            if servico.id > 26429:
                print(servico.id)
                chapa = Chapa.objects.get(pk=servico.chapa.id)
                valor_total = servico.quantidade * chapa.valor
                servico.valor_total_servico = valor_total
                servico.save(update_fields=['valor_total_servico'])
