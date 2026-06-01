from .models import ItemCardapio
from .dto import ItemCardapioDTO
from typing import Optional

class CardapioService:
    @staticmethod
    def get_item_por_id(item_id: int) -> Optional[ItemCardapioDTO]:
        try:
            item = ItemCardapio.objects.get(id=item_id)
            return ItemCardapioDTO(
                id=item.id,
                nome=item.nome,
                preco=item.preco,
                disponivel=item.disponivel
            )
        except ItemCardapio.DoesNotExist:
            return None

    @staticmethod
    def verificar_disponibilidade(item_id: int) -> bool:
        item = ItemCardapio.objects.filter(id=item_id).first()
        return item.disponivel if item else False
