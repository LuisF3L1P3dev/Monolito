from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class ItemCardapioDTO:
    id: int
    nome: str
    preco: Decimal
    disponivel: bool
