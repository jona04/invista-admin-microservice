from django.core.management import BaseCommand

from core.models import Nota, GrupoNotaServico, Servico

class Command(BaseCommand):
    def handle(self, *args, **kargs):
        for nota in Nota.objects.all():
            if nota.id > 16517:
                print(nota.id)
                gropo_nota_servicos = GrupoNotaServico.objects.filter(nota_id=nota.id)
                valor_total = 0
                for nota_servico in gropo_nota_servicos:
                    servico = Servico.objects.get(pk=nota_servico.servico.id)
                    servico_total = servico.valor_total_servico if servico.valor_total_servico is not None else 0
                    valor_total = valor_total + servico_total
                nota.valor_total_nota = valor_total
                nota.save(update_fields=['valor_total_nota'])