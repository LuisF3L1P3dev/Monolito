import os
import django
import time

# Configuração para rodar script standalone com Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from cardapio.models import ItemCardapio
from pedidos.models import Pedido, ItemPedido
from pedidos.services import PedidoService
from pagamento.services import PagamentoPadraoService, PagamentoRapidoService
from notificacao.services import NotificacaoService

def criar_cenario_teste(nome_item, preco):
    item, _ = ItemCardapio.objects.get_or_create(nome=nome_item, defaults={'preco': preco, 'disponivel': True})
    pedido = Pedido.objects.create()
    # No monólito modular, capturamos o preço no momento da criação do item do pedido
    ItemPedido.objects.create(pedido=pedido, item_cardapio_id=item.id, quantidade=1, preco_unitario=item.preco)
    pedido.calcular_total()
    return pedido

def rodar_teste_comparativo():
    print("\n=== INICIANDO TESTE COMPARATIVO DE PAGAMENTO ===\n")

    # TESTE 1: Pagamento Padrão (Lento)
    print("--- CENÁRIO 1: Pagamento PADRÃO (com delay de 5s) ---")
    pedido1 = criar_cenario_teste("Pizza Modular", 50.0)
    print(f"Pedido #{pedido1.id} criado. Total: R$ {pedido1.total}")
    
    inicio = time.time()
    servico_padrao = PagamentoPadraoService()
    if servico_padrao.processar_pagamento(pedido1.id, pedido1.total):
        NotificacaoService.notificar_cozinha(pedido1.id)
        fim = time.time()
        print(f"Resultado: Pedido #{pedido1.id} processado em {fim - inicio:.2f} segundos.")
    
    print("\n" + "="*50 + "\n")

    # TESTE 2: Pagamento Rápido (Instantâneo)
    print("--- CENÁRIO 2: Pagamento RÁPIDO (sem delay) ---")
    pedido2 = criar_cenario_teste("Suco Modular", 10.0)
    print(f"Pedido #{pedido2.id} criado. Total: R$ {pedido2.total}")
    
    inicio = time.time()
    servico_rapido = PagamentoRapidoService()
    if servico_rapido.processar_pagamento(pedido2.id, pedido2.total):
        NotificacaoService.notificar_cozinha(pedido2.id)
        fim = time.time()
        print(f"Resultado: Pedido #{pedido2.id} processado em {fim - inicio:.2f} segundos.")

    print("\n=== TESTE COMPARATIVO FINALIZADO ===\n")
    print("Observe como o comportamento mudou trocando apenas a implementação do Service,")
    print("sem alterar nenhuma linha de código nos módulos de Pedidos ou Notificação.")

if __name__ == "__main__":
    try:
        rodar_teste_comparativo()
    except Exception as e:
        print(f"\nERRO AO RODAR TESTE: {e}")
        import traceback
        traceback.print_exc()
