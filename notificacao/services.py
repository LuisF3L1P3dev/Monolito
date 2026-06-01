from .models import LogNotificacao
from pedidos.services import PedidoService

class NotificacaoService:
    @staticmethod
    def notificar_cozinha(pedido_id: int):
        # Busca dados via Service externo, não via Model direto
        pedido = PedidoService.get_pedido_por_id(pedido_id)

        if not pedido:
            print(f"[COZINHA] ERRO: Pedido #{pedido_id} não encontrado.")
            return

        if pedido.status == 'PAGO':
            mensagem = f"Pedido #{pedido.id} processado com sucesso. Preparar itens!"
            print(f"\n[COZINHA] ---> ALERTA: {mensagem} <--- \n")
            
            # Salva no banco local do módulo
            LogNotificacao.objects.create(pedido_id=pedido_id, mensagem=mensagem)
            
            # Atualiza status via Service do módulo de pedidos
            PedidoService.atualizar_status(pedido_id, 'ENVIADO_COZINHA')
        else:
            print(f"\n[COZINHA] ---> ERRO: Pedido #{pedido.id} recusado. Status atual: {pedido.status} <--- \n")
