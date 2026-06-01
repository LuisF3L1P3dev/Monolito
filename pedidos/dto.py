from dataclasses import dataclass
from decimal import Decimal
from typing import List

@dataclass(frozen=True)
class ItemPedidoDTO:
    item_id: int
    nome: str
    quantidade: int
    preco_unitario: Decimal

@dataclass(frozen=True)
class PedidoDTO:
    id: int
    status: str
    total: Decimal
    itens: List[ItemPedidoDTO]
