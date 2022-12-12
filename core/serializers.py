from attr import fields
from rest_framework import serializers
# pylint: disable=import-error
from core.models import (Chapa, GrupoNotaServico, Nota, Servico, 
    Cliente, EntradaChapa, SaidaChapa, CategoriaEntrada, CategoriaSaida)


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = (
            "id",
            "nome",
            "email",
            "telefone",
            "cnpj",
            "cpf",
            "rua",
            "bairro",
            "numero",
            "cidade",
            "estado",
            "cep",
            "created_at",
            "uploaded_at"
        )


class ChapaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapa
        fields = ("id", "nome", "valor", "estoque", "obs", "created_at", "uploaded_at")


class ChapaEstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapa
        fields = ("id","nome", "estoque")


class EntradaChapaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntradaChapa
        fields = ("id", "quantidade", "marca", "valor_unitario", "chapa", "categoria", "data", "created_at", "observacao")


class SaidaChapaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaidaChapa
        fields = ("id", "quantidade", "observacao", "chapa", "categoria", "data", "created_at", "observacao")


class CategoriaEntradaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaEntrada
        fields = ("id", "descricao")


class CategoriaSaidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaSaida
        fields = ("id", "descricao")


class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = (
            "id",
            "nome",
            "cliente",
            "chapa",
            "quantidade",
            "valor_total_servico",
            "created_at",
            "uploaded_at",
        )


class ServicoFullSerializer(serializers.ModelSerializer):
    chapa = ChapaSerializer()
    cliente = ClienteSerializer()
    class Meta:
        model = Servico
        fields = (
            "id",
            "nome",
            "cliente",
            "chapa",
            "quantidade",
            "valor_total_servico",
            "created_at",
            "uploaded_at",
        )


class ServicoCreateNotaSerializer(serializers.ModelSerializer):
    chapa = serializers.StringRelatedField()
    class Meta:
        model = Servico
        fields = (
            "id",
            "nome",
            "chapa",
            "quantidade",
            "valor_total_servico",
            "created_at",
            "uploaded_at",
        )


class ServicoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = (
            "id",
            "nome",
            "quantidade",
            "valor_total_servico",
            "created_at"
        )


class NotaFullSerializer(serializers.ModelSerializer):
    servico = ServicoFullSerializer(many=True)
    class Meta:
        model = Nota
        fields = (
            "id",
            "desconto",
            "numero",
            "obs",
            "servico",
            "status",
            "valor_total_nota",
            "created_at"
        )


class NotaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = (
            "id",
            "desconto",
            "numero",
            "obs",
            "status",
            "valor_total_nota",
            "created_at"
        )


class NotaRelatorioSerializer(serializers.ModelSerializer):
    servico = ServicoFullSerializer(many=True)
    class Meta:
        model = Nota
        fields = (
            "id",
            "servico",
            "valor_total_nota",
            "created_at"
        )


class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = (
            "id",
            "desconto",
            "numero",
            "obs",
            "servico",
            "status",
            "valor_total_nota",
            "created_at",
            "uploaded_at",
        )


class GrupoNotaServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoNotaServico
        fields = (
            "id",
            "nota",
            "servico"
        )
