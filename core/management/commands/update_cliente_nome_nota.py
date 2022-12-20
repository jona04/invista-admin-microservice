from django.core.management import BaseCommand

from core.models import Nota, GrupoNotaServico, Servico, GrupoClienteNota

class Command(BaseCommand):
    def handle(self, *args, **kargs):
        for nota in Nota.objects.all():
            # if nota.id > 16517:
            print(nota.id)
            gropo_nota_servicos = GrupoNotaServico.objects.filter(nota_id=nota.id)
            if len(gropo_nota_servicos) > 0:
                cliente_nome = gropo_nota_servicos[0].servico.cliente.nome
                nota.cliente_nome = cliente_nome
                nota.save(update_fields=['cliente_nome'])