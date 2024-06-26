from attr import fields
from rest_framework import serializers
# pylint: disable=import-error
from core.models import (Chapa, GrupoNotaServico, Nota, Servico, 
    Cliente, EntradaChapa, SaidaChapa, CategoriaEntrada, CategoriaSaida,
    GrupoClienteNota, User)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'is_financeiro']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance
    
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


class CategoriaEntradaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaEntrada
        fields = ("id", "descricao")


class CategoriaSaidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaSaida
        fields = ("id", "descricao")


class EntradaChapaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntradaChapa
        fields = ("id", "quantidade", "marca", "valor_unitario", "chapa", "categoria", "data", "created_at", "observacao")


class SaidaChapaListSerializer(serializers.ModelSerializer):
    chapa = ChapaSerializer()
    categoria = CategoriaEntradaSerializer()
    class Meta:
        model = EntradaChapa
        fields = ("id", "quantidade", "observacao", "chapa", "categoria", "data", "created_at", "observacao")


class EntradaChapaListSerializer(serializers.ModelSerializer):
    chapa = ChapaSerializer()
    categoria = CategoriaEntradaSerializer()
    class Meta:
        model = EntradaChapa
        fields = ("id", "quantidade", "marca", "valor_unitario", "chapa", "categoria", "data", "created_at", "observacao")


class SaidaChapaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaidaChapa
        fields = ("id", "quantidade", "observacao", "chapa", "categoria", "data", "created_at", "observacao")


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
    chapa = ChapaSerializer()
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
            "cliente_nome",
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
            "cliente_nome",
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
            "cliente_nome",
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
            "cliente_nome",
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

class GrupoNotaClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoClienteNota
        fields = (
            "id",
            "nota",
            "cliente"
        )
