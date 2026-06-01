from dataclasses import dataclass
from decimal import Decimal
from typing import List

# Data Transfer Object - Serve como contrato de dados entre os módulos
# @dataclass(frozen=True) -> Torna o DTO imutável, garantindo que os dados não sejam modificados inesperadamente
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
