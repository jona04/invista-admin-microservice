from django.core.management import BaseCommand

from core.models import GrupoClienteNota

class Command(BaseCommand):
    def handle(self, *args, **options):
        nota_clientes = GrupoClienteNota.objects.using('old').all()

        for nota_cliente in nota_clientes:
            if nota_cliente.id > 16388:
                print(nota_cliente.id)
                GrupoClienteNota.objects.create(
                    nota = nota_cliente.nota,
                    cliente = nota_cliente.cliente
                )

