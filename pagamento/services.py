import time
from decimal import Decimal
from .interfaces import PagamentoInterface
from .models import Transacao
from pedidos.services import PedidoService

class PagamentoPadraoService(PagamentoInterface):
    def processar_pagamento(self, pedido_id: int, valor: Decimal) -> bool:
        # [EXPERIMENTO] Simula lentidão
        print(f"Processando pagamento PADRÃO do pedido #{pedido_id}... (5s)")
        time.sleep(5)
        
        # Cria registro interno do módulo
        # Nota: PedidoService é usado apenas para validação lógica, não para acesso direto ao DB de pedidos
        transacao, _ = Transacao.objects.get_or_create(pedido_id=pedido_id, defaults={'valor': valor})
        transacao.status = 'APROVADO'
        transacao.save()
        
        # Comunicação via interface pública do módulo de pedidos
        return PedidoService.marcar_como_pago(pedido_id)

    def consultar_status(self, pedido_id: int) -> str:
        transacao = Transacao.objects.filter(pedido_id=pedido_id).first()
        return transacao.status if transacao else "NÃO ENCONTRADO"

class PagamentoRapidoService(PagamentoInterface):
    def processar_pagamento(self, pedido_id: int, valor: Decimal) -> bool:
        # [EXPERIMENTO] Sem lentidão
        print(f"Processando pagamento RÁPIDO do pedido #{pedido_id}...")
        
        transacao, _ = Transacao.objects.get_or_create(pedido_id=pedido_id, defaults={'valor': valor})
        transacao.status = 'APROVADO'
        transacao.save()
        
        return PedidoService.marcar_como_pago(pedido_id)

    def consultar_status(self, pedido_id: int) -> str:
        transacao = Transacao.objects.filter(pedido_id=pedido_id).first()
        return transacao.status if transacao else "NÃO ENCONTRADO"
