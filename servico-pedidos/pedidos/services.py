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
    Erros 5xx são transientes (retenta). Erros 4xx são definitivos (não retenta).
    """
    url = f"{settings.PAGAMENTO_URL}/api/pagamentos/processar/"
    payload = {'pedido_id': pedido_id, 'valor': str(valor)}
    max_tentativas = 3
    ultimo_erro = 'Serviço de pagamento indisponível'

    for tentativa in range(1, max_tentativas + 1):
        try:
            print(f"[PEDIDOS] Tentativa {tentativa}/{max_tentativas} — chamando pagamento...")
            resp = requests.post(url, json=payload, timeout=HTTP_TIMEOUT)
            if resp.status_code == 200:
                return {'sucesso': True, 'dados': resp.json()}
            if resp.status_code < 500:
                # 4xx: erro definitivo do cliente, não retenta
                return {'sucesso': False, 'mensagem': f"Pagamento recusou com status {resp.status_code}"}
            # 5xx: erro transiente do servidor, retenta
            ultimo_erro = f"Erro {resp.status_code} no serviço de pagamento"
        except requests.exceptions.Timeout:
            ultimo_erro = 'Timeout no serviço de pagamento'
        except requests.exceptions.ConnectionError:
            ultimo_erro = 'Serviço de pagamento indisponível'

        if tentativa < max_tentativas:
            espera = 2 ** (tentativa - 1)  # 1s, 2s
            print(f"[PEDIDOS] {ultimo_erro} na tentativa {tentativa}. Aguardando {espera}s...")
            time.sleep(espera)

    return {'sucesso': False, 'mensagem': f"{ultimo_erro} após {max_tentativas} tentativas"}
