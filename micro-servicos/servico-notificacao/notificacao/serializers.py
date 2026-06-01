from rest_framework import serializers
from .models import LogNotificacao


class LogNotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogNotificacao
        fields = ['id', 'pedido_id', 'mensagem', 'data_envio']
