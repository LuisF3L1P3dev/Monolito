from pedidos.models import Pedido
from .models import LogNotificacao

def notificar_cozinha(pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)

    # Regra de negócio: Só notifica a cozinha se o pagamento foi confirmado
    if pedido.status == 'PAGO':
        mensagem = f"Pedido #{pedido.id} processado com sucesso. Preparar itens!"
        print(f"\n[COZINHA] ---> ALERTA: {mensagem} <--- \n")
        
        # Salva o log de notificação no banco
        LogNotificacao.objects.create(pedido=pedido, mensagem=mensagem)
        
        # Atualiza o status do pedido para 'Enviado à Cozinha'
        pedido.status = 'ENVIADO_COZINHA'
        pedido.save(update_fields=['status'])
    else:
        print(f"\n[COZINHA] ---> ERRO: Pedido #{pedido.id} recusado. Status atual: {pedido.status} <--- \n")