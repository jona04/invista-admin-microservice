from rest_framework import exceptions
from .models import Cliente, Chapa, Servico, Nota, GrupoNotaServico

def cliente_created(data):
    Cliente.objects.create(
        id = data['id'],
        nome = data['nome'],
        email = data['email'],
        telefone = data['telefone'],
        cnpj = data['cnpj'],
        cpf = data['cpf'],
        rua = data['rua'],
        bairro = data['bairro'],
        numero = data['numero'],
        cidade = data['cidade'],
        estado = data['estado'],
        cep = data['cep'],
        created_at = data['created_at'],
        uploaded_at = data['uploaded_at']
    )

def cliente_updated(data):
    cliente = Cliente.objects.get(pk=data['id'])

    cliente.nome = data['nome']
    cliente.email = data['email']
    cliente.telefone = data['telefone']
    cliente.cnpj = data['cnpj']
    cliente.cpf = data['cpf']
    cliente.rua = data['rua']
    cliente.bairro = data['bairro']
    cliente.numero = data['numero']
    cliente.cidade = data['cidade']
    cliente.estado = data['estado']
    cliente.cep = data['cep']
    cliente.created_at = data['created_at']
    cliente.uploaded_at = data['uploaded_at']
    cliente.save()

def cliente_deleted(pk):
    Cliente.objects.delete(pk=pk)

def chapa_created(data):
    Chapa.objects.create(
        id = data['id'],
        nome = data['nome'],
        estoque = data['estoque'],
        marca = data['marca'],
        obs = data['obs'],
        created_at = data['created_at'],
        uploaded_at = data['uploaded_at'],
    )

def chapa_updated(data):
    chapa = Chapa.objects.get(pk=data['id'])
    
    chapa.nome = data['nome']
    chapa.estoque = data['estoque']
    chapa.marca = data['marca']
    chapa.obs = data['obs']
    chapa.created_at = data['created_at']
    chapa.uploaded_at = data['uploaded_at']

def chapa_deleted(pk):
    Chapa.objects.delete(pk=pk)

def servico_created(data):
    cliente = Cliente.objects.get(pk=data['cliente'])
    chapa = Chapa.objects.get(pk=data['chapa'])
    Servico.objects.create(
        id = data['id'],
        nome = data['nome'],
        cliente = cliente,
        chapa =  chapa,
        quantidade = data['quantidade'],
        created_at = data['created_at'],
        uploaded_at = data['uploaded_at'],
        valor_total_servico = data['valor_total_servico']
    )

def servico_updated(data):
    cliente = Cliente.objects.get(pk=data['cliente'])
    chapa = Chapa.objects.get(pk=data['chapa'])
    servico = Servico.objects.get(pk=data['id'])

    servico.nome = data['nome']
    servico.cliente = cliente
    servico.chapa =  chapa
    servico.quantidade = data['quantidade']
    servico.created_at = data['created_at']
    servico.uploaded_at = data['uploaded_at']
    servico.valor_total_servico = data['valor_total_servico']
    servico.save()

def servico_deleted(pk):
    Servico.objects.delete(pk=pk)

def nota_created(data):
    Nota.objects.create(
        id = data['id'],
        desconto = data['desconto'],
        created_at = data['created_at'],
        uploaded_at = data['uploaded_at'],
        obs = data['obs'],
        valor_total_nota = data['valor_total_nota']
    )

def nota_created(data):
    nota = Nota.objects.get(pk=data['id'])

    nota.id = data['id'],
    nota.desconto = data['desconto'],
    nota.created_at = data['created_at'],
    nota.uploaded_at = data['uploaded_at'],
    nota.obs = data['obs'],
    nota.valor_total_nota = data['valor_total_nota']
    nota.save()

def nota_deleted(pk):
    Nota.objects.delete(pk=pk)

def grupo_nota_servico_created(data):
    nota = Nota.objects.get(pk=data['nota'])
    servico = Servico.objects.get(pk=data['servico'])
    GrupoNotaServico.objects.create(
        id = data['id'],
        nota = nota,
        servico = servico
    )

def grupo_nota_servico_created(pk):
    GrupoNotaServico.objects.delete(pk=pk)
