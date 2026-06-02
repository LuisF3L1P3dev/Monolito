from rest_framework import serializers
from .models import Transacao


class TransacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transacao
        fields = ['id', 'pedido_id', 'valor', 'status', 'data_transacao']


class ProcessarPagamentoSerializer(serializers.Serializer):
    pedido_id = serializers.IntegerField()
    valor = serializers.DecimalField(max_digits=10, decimal_places=2)
