from django.core.management import BaseCommand

from core.models import Cliente

class Command(BaseCommand):
    def handle(self, *args, **options):
        clientes = Cliente.objects.using('old').all()

        for cliente in clientes:
            Cliente.objects.create(
                id = cliente.id,
                nome = cliente.nome,
                email = cliente.email,
                telefone = cliente.telefone,
                cnpj = cliente.cnpj,
                cpf = cliente.cpf,
                rua = cliente.rua,
                bairro = cliente.bairro,
                numero = cliente.numero,
                cidade = cliente.cidade,
                estado = cliente.estado,
                cep = cliente.cep,
                created_at = cliente.created_at,
                uploaded_at = cliente.uploaded_at
            )

