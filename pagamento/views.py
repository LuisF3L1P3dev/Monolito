import time
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from pedidos.models import Pedido
from pagamento.models import Transacao
from notificacao.services import notificar_cozinha

class ProcessarPagamentoView(View):
    def post(self, request, pedido_id):
        pedido = get_object_or_404(Pedido, id=pedido_id)
        
        # Cria ou recupera a transação
        transacao, _ = Transacao.objects.get_or_create(pedido=pedido)

        # [CHECK-04] INJEÇÃO DE LATÊNCIA: simula a demora do pagamento
        print(f"Processando pagamento do pedido #{pedido_id}... (Aguarde 5 segundos)")
        time.sleep(5) 
        
        # Simula a aprovação do pagamento
        transacao.status = 'APROVADO'
        transacao.save()

        # Atualiza status do pedido indicando que está pago
        pedido.status = 'PAGO'
        pedido.save(update_fields=['status'])

        # [CHECK-03] Chamada síncrona de notificação (acoplamento)
        notificar_cozinha(pedido_id)
        
        # Redireciona de volta para a lista de pedidos após finalizar
        return HttpResponseRedirect(reverse('pedidos-list'))