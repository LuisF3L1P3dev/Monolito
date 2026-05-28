from pedidos.models import Pedido
from .models import LogNotificacao

def notificar_cozinha(pedido_id):
    mensagem = f"Pedido #{pedido_id} processado com sucesso. Preparar itens!"
    print(f"\n[COZINHA] ---> ALERTA: {mensagem} <--- \n")