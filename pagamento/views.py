from django.views.generic import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .services import PagamentoPadraoService # Poderia ser injetado ou via Factory
from pedidos.services import PedidoService
from notificacao.services import NotificacaoService

class ProcessarPagamentoView(View):
    def post(self, request, pedido_id):
        # Busca dados via PedidoService (DTO)
        pedido_dto = PedidoService.get_pedido_por_id(pedido_id)
        if not pedido_dto:
            return HttpResponseRedirect(reverse('pedidos-list'))
        
        # [EXPERIMENTO] Para trocar a implementação, altere a classe abaixo:
        # PagamentoPadraoService() -> Possui delay de 5s
        # PagamentoRapidoService() -> Sem delay
        pagamento_service = PagamentoPadraoService()
        
        sucesso = pagamento_service.processar_pagamento(pedido_id, pedido_dto.total)

        if sucesso:
            # Notificação via Service
            NotificacaoService.notificar_cozinha(pedido_id)
        
        return HttpResponseRedirect(reverse('pedidos-list'))