from .models import Pedido
from .dto import PedidoDTO, ItemPedidoDTO
from cardapio.services import CardapioService
from typing import Optional

class PedidoService:
    @staticmethod
    def get_pedido_por_id(pedido_id: int) -> Optional[PedidoDTO]:
        try:
            pedido = Pedido.objects.get(id=pedido_id)
            itens_dto = []
            for ip in pedido.itens.all():
                # Busca detalhes do item via API pública do Cardápio
                item_cardapio = CardapioService.get_item_por_id(ip.item_cardapio_id)
                if item_cardapio:
                    itens_dto.append(ItemPedidoDTO(
                        item_id=ip.item_cardapio_id,
                        nome=item_cardapio.nome,
                        quantidade=ip.quantidade,
                        preco_unitario=ip.preco_unitario  # snapshot capturado no momento do pedido
                    ))
            
            return PedidoDTO(
                id=pedido.id,
                status=pedido.status,
                total=pedido.total,
                itens=itens_dto
            )
        except Pedido.DoesNotExist:
            return None

    @staticmethod
    def marcar_como_pago(pedido_id: int) -> bool:
        try:
            pedido = Pedido.objects.get(id=pedido_id)
            pedido.status = 'PAGO'
            pedido.save(update_fields=['status'])
            return True
        except Pedido.DoesNotExist:
            return False

    @staticmethod
    def atualizar_status(pedido_id: int, novo_status: str) -> bool:
        try:
            pedido = Pedido.objects.get(id=pedido_id)
            pedido.status = novo_status
            pedido.save(update_fields=['status'])
            return True
        except Pedido.DoesNotExist:
            return False
