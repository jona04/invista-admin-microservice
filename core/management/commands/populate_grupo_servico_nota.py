from django.core.management import BaseCommand

from core.models import GrupoNotaServico

class Command(BaseCommand):
    def handle(self, *args, **options):
        nota_servicos = GrupoNotaServico.objects.using('old').all()

        for nota_servico in nota_servicos:
            if(nota_servico.id > 26286):
                print(nota_servico.id)
                GrupoNotaServico.objects.create(
                    id = nota_servico.id,
                    nota = nota_servico.nota,
                    servico = nota_servico.servico
                )

