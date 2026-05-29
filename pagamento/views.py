import time
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from notificacao.services import notificar_cozinha

class ProcessarPagamentoView(View):
    def post(self, request, pedido_id):
        # [CHECK-04] INJEÇÃO DE LATÊNCIA: simula a demora do pagamento
        print(f"Processando pagamento do pedido #{pedido_id}... (Aguarde 5 segundos)")
        time.sleep(5) 
        
        # [CHECK-03] Chamada síncrona de notificação (acoplamento)
        notificar_cozinha(pedido_id)
        
        # Redireciona de volta para a lista de pedidos após finalizar
        return HttpResponseRedirect(reverse('pedidos-list'))