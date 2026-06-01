from abc import ABC, abstractmethod
from decimal import Decimal

class PagamentoInterface(ABC):
    @abstractmethod
    def processar_pagamento(self, pedido_id: int, valor: Decimal) -> bool:
        pass

    @abstractmethod
    def consultar_status(self, pedido_id: int) -> str:
        pass
