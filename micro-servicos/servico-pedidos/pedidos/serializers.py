from rest_framework import serializers
from .models import Pedido, ItemPedido


class ItemPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = ['id', 'item_cardapio_id', 'nome_item', 'quantidade', 'preco_unitario']


class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'data_criacao', 'status', 'total', 'observacao', 'itens']


class CriarPedidoItemSerializer(serializers.Serializer):
    item_cardapio_id = serializers.IntegerField()
    quantidade = serializers.IntegerField(min_value=1)


class CriarPedidoSerializer(serializers.Serializer):
    itens = CriarPedidoItemSerializer(many=True)
    observacao = serializers.CharField(required=False, allow_blank=True)
