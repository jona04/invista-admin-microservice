from typing import Any, Dict
from rest_framework import serializers

from core.models import Chapa, Servico


class ChapaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapa
        fields = ("id", "nome", "valor", "estoque", "obs", "created_at", "uploaded_at")


class ServicoSerializer(serializers.ModelSerializer):
    cliente = serializers.StringRelatedField()
    chapa = serializers.StringRelatedField()

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


class ServicoSerializerTest():

    def serialize_servico(servico: Servico) -> Dict[str, Any]:
        return {
            'nome': servico.nome,
            'cliente': servico.cliente.__str__(),
            'chapa': servico.chapa.__str__(),
            'quantidade': servico.quantidade,
            'valor_total_servico': servico.valor_total_servico,
            'created_at': servico.created_at.isoformat()
        }
