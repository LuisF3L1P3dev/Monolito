import os
import django
import time

# Configuração para rodar script standalone com Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from cardapio.models import ItemCardapio
from pedidos.models import Pedido, ItemPedido
from pagamento.models import Transacao
from notificacao.services import notificar_cozinha

def rodar_teste_monolito():
    print("\n=== INICIANDO TESTE DO MONÓLITO ===\n")

    # 1. Criação do Item e do Pedido
    # Garante que temos um item no cardápio
    item, _ = ItemCardapio.objects.get_or_create(
        nome="Hambúrguer de Teste", 
        defaults={'preco': 25.0, 'descricao': 'Hambúrguer para teste automatizado', 'disponivel': True}
    )
    
    # Cria um novo pedido pendente
    pedido = Pedido.objects.create()
    
    # Adiciona o item ao pedido (isso dispara o cálculo do total no model)
    ItemPedido.objects.create(pedido=pedido, item_cardapio=item, quantidade=2)
    
    # Recarrega do banco para garantir que temos o total atualizado
    pedido.refresh_from_db()
    print(f"Pedido #{pedido.id} criado com status: {pedido.status}")
    print(f"Total calculado: R$ {pedido.total}")

    inicio = time.time()

    # 2. Simulação do fluxo de pagamento (Lógica extraída do admin.py)
    print("\n[PAGAMENTO] Iniciando processamento...")
    transacao, _ = Transacao.objects.get_or_create(pedido=pedido)
    
    # Simula latência de API de pagamento (5 segundos)
    print("Aguardando confirmação da operadora (5s)...")
    time.sleep(5)
    
    transacao.status = 'APROVADO'
    transacao.save()
    
    pedido.status = 'PAGO'
    pedido.save(update_fields=['status'])
    print(f"[PAGAMENTO] Transação aprovada para o Pedido #{pedido.id}")

    # 3. Notificação da Cozinha (Chamada direta/acoplada do serviço)
    print("\n[NOTIFICAÇÃO] Chamando serviço de cozinha...")
    notificar_cozinha(pedido.id)

    fim = time.time()
    
    # Validação Final
    pedido.refresh_from_db()
    print(f"\nResultado Final:")
    print(f"- Status do Pedido: {pedido.status}")
    print(f"- Tempo decorrido: {fim - inicio:.2f} segundos")
    
    if pedido.status == 'ENVIADO_COZINHA':
        print("\nSUCESSO: O fluxo do monólito foi executado corretamente.")
    else:
        print("\nFALHA: O pedido não chegou ao status esperado.")

    print("\n=== TESTE DO MONÓLITO FINALIZADO ===\n")

if __name__ == "__main__":
    try:
        rodar_teste_monolito()
    except Exception as e:
        print(f"\nERRO AO RODAR TESTE: {e}")
        import traceback
        traceback.print_exc()
