from django.core.management import BaseCommand

from core.models import Servico

class Command(BaseCommand):
    def handle(self, *args, **options):
        servicos_old = Servico.objects.using('old').all().order_by('id')

        for servico_old in servicos_old:
            print(servico_old.id)
            servico = Servico.objects.get(pk=servico_old.id)
            servico.created_at = servico_old.created_at
            servico.save()
    
