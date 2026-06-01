import time
import requests
from django.conf import settings

# Timeout explícito em todas as chamadas HTTP (estratégia de resiliência)
HTTP_TIMEOUT = 10


def get_item_cardapio(item_id: int) -> dict | None:
    url = f"{settings.CARDAPIO_URL}/api/cardapio/{item_id}/"
    try:
        resp = requests.get(url, timeout=HTTP_TIMEOUT)
        if resp.status_code == 200:
            return resp.json()
        return None
    except requests.exceptions.RequestException as e:
        print(f"[PEDIDOS] Erro ao consultar cardapio item {item_id}: {e}")
        return None


def processar_pagamento(pedido_id: int, valor) -> dict:
    """
    Chama o servico-pagamento com retry + backoff exponencial.
    Retorna dict com 'sucesso' e 'mensagem'.
    """
    url = f"{settings.PAGAMENTO_URL}/api/pagamentos/processar/"
    payload = {'pedido_id': pedido_id, 'valor': str(valor)}
    max_tentativas = 3

    for tentativa in range(1, max_tentativas + 1):
        try:
            print(f"[PEDIDOS] Tentativa {tentativa}/{max_tentativas} — chamando pagamento...")
            resp = requests.post(url, json=payload, timeout=HTTP_TIMEOUT)
            if resp.status_code == 200:
                return {'sucesso': True, 'dados': resp.json()}
            return {'sucesso': False, 'mensagem': f"Pagamento recusou com status {resp.status_code}"}
        except requests.exceptions.Timeout:
            if tentativa < max_tentativas:
                espera = 2 ** (tentativa - 1)  # 1s, 2s, 4s
                print(f"[PEDIDOS] Timeout na tentativa {tentativa}. Aguardando {espera}s...")
                time.sleep(espera)
            else:
                return {'sucesso': False, 'mensagem': 'Serviço de pagamento não respondeu após 3 tentativas'}
        except requests.exceptions.ConnectionError:
            if tentativa < max_tentativas:
                espera = 2 ** (tentativa - 1)
                print(f"[PEDIDOS] Conexão recusada na tentativa {tentativa}. Aguardando {espera}s...")
                time.sleep(espera)
            else:
                return {'sucesso': False, 'mensagem': 'Serviço de pagamento indisponível'}
