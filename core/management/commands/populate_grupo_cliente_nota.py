from django.core.management import BaseCommand

from core.models import GrupoClienteNota

class Command(BaseCommand):
    def handle(self, *args, **options):
        nota_clientes = GrupoClienteNota.objects.using('old').all()

        for nota_cliente in nota_clientes:
            GrupoClienteNota.objects.create(
                id = nota_cliente.id,
                nota = nota_cliente.nota,
                cliente = nota_cliente.cliente
            )

