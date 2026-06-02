from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Pedido, ItemPedido
from .serializers import PedidoSerializer, CriarPedidoSerializer
from . import services


class PedidoListCreateView(APIView):
    def get(self, request):
        pedidos = Pedido.objects.prefetch_related('itens').all()
        return Response(PedidoSerializer(pedidos, many=True).data)

    def post(self, request):
        serializer = CriarPedidoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        itens_input = serializer.validated_data['itens']
        observacao = serializer.validated_data.get('observacao', '')

        # Valida disponibilidade e coleta preços via servico-cardapio
        itens_resolvidos = []
        for item_input in itens_input:
            item = services.get_item_cardapio(item_input['item_cardapio_id'])
            if not item:
                return Response(
                    {'erro': f"Item {item_input['item_cardapio_id']} não encontrado no cardápio"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not item.get('disponivel'):
                return Response(
                    {'erro': f"Item '{item['nome']}' não está disponível"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            itens_resolvidos.append({
                'item_cardapio_id': item['id'],
                'nome_item': item['nome'],
                'quantidade': item_input['quantidade'],
                'preco_unitario': Decimal(str(item['preco'])),
            })

        total = sum(i['preco_unitario'] * i['quantidade'] for i in itens_resolvidos)

        pedido = Pedido.objects.create(total=total, observacao=observacao)
        for i in itens_resolvidos:
            ItemPedido.objects.create(pedido=pedido, **i)

        return Response(PedidoSerializer(pedido).data, status=status.HTTP_201_CREATED)


class PedidoDetailView(APIView):
    def get(self, request, pk):
        try:
            pedido = Pedido.objects.prefetch_related('itens').get(pk=pk)
        except Pedido.DoesNotExist:
            return Response({'erro': 'Pedido não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response(PedidoSerializer(pedido).data)

    def delete(self, request, pk):
        try:
            pedido = Pedido.objects.get(pk=pk)
        except Pedido.DoesNotExist:
            return Response({'erro': 'Pedido não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        pedido.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PedidoPagarView(APIView):
    def post(self, request, pk):
        try:
            pedido = Pedido.objects.get(pk=pk)
        except Pedido.DoesNotExist:
            return Response({'erro': 'Pedido não encontrado'}, status=status.HTTP_404_NOT_FOUND)

        if pedido.status != 'PENDENTE':
            return Response(
                {'erro': f"Pedido já está com status '{pedido.status}'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Chama servico-pagamento com retry + timeout (resiliência)
        resultado = services.processar_pagamento(pedido.id, pedido.total)

        if resultado['sucesso']:
            pedido.status = 'PAGO'
            pedido.save(update_fields=['status'])
            return Response({'mensagem': 'Pagamento aprovado e pedido enviado para a cozinha', 'pedido_id': pedido.id})

        return Response({'erro': resultado.get('mensagem', 'Falha no pagamento')}, status=status.HTTP_502_BAD_GATEWAY)


class PedidoCancelarView(APIView):
    def post(self, request, pk):
        try:
            pedido = Pedido.objects.get(pk=pk)
        except Pedido.DoesNotExist:
            return Response({'erro': 'Pedido não encontrado'}, status=status.HTTP_404_NOT_FOUND)

        if pedido.status in ('PAGO', 'ENVIADO_COZINHA'):
            return Response(
                {'erro': f"Não é possível cancelar pedido com status '{pedido.status}'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        pedido.status = 'CANCELADO'
        pedido.save(update_fields=['status'])
        return Response({'mensagem': 'Pedido cancelado', 'pedido_id': pedido.id})
