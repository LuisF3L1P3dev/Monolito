from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transacao
from .serializers import ProcessarPagamentoSerializer, TransacaoSerializer
from . import services


class ProcessarPagamentoView(APIView):
    def post(self, request):
        serializer = ProcessarPagamentoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        pedido_id = serializer.validated_data['pedido_id']
        valor = serializer.validated_data['valor']

        # Idempotência: não reprocessa pedido já pago
        transacao_existente = Transacao.objects.filter(pedido_id=pedido_id).first()
        if transacao_existente and transacao_existente.status == 'APROVADO':
            return Response({'sucesso': True, 'status': 'APROVADO', 'pedido_id': pedido_id})

        transacao, _ = Transacao.objects.get_or_create(
            pedido_id=pedido_id,
            defaults={'valor': valor},
        )
        transacao.status = 'APROVADO'
        transacao.save(update_fields=['status'])

        mensagem = f"Pedido #{pedido_id} confirmado (R$ {valor}). Preparar itens!"
        services.publicar_notificacao_fila(pedido_id, mensagem)

        return Response({'sucesso': True, 'status': 'APROVADO', 'pedido_id': pedido_id})


class StatusPagamentoView(APIView):
    def get(self, request, pedido_id):
        transacao = Transacao.objects.filter(pedido_id=pedido_id).first()
        if not transacao:
            return Response({'erro': 'Transação não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        return Response(TransacaoSerializer(transacao).data)
