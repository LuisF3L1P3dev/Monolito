import json
import time
import pika
from django.conf import settings
from .models import LogNotificacao


def _callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        pedido_id = data['pedido_id']
        mensagem = data['mensagem']

        LogNotificacao.objects.create(pedido_id=pedido_id, mensagem=mensagem)
        print(f"\n[COZINHA] ---> ALERTA: {mensagem} <---\n")

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"[NOTIFICACAO] Erro ao processar mensagem: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def consumir():
    """Loop de consumo com reconexão automática em caso de falha."""
    rabbitmq_url = settings.RABBITMQ_URL

    while True:
        try:
            params = pika.URLParameters(rabbitmq_url)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()

            channel.queue_declare(queue='notificacao_cozinha', durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue='notificacao_cozinha', on_message_callback=_callback)

            print('[NOTIFICACAO] Aguardando mensagens da fila notificacao_cozinha...')
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError as e:
            print(f"[NOTIFICACAO] Conexão perdida: {e}. Reconectando em 5s...")
            time.sleep(5)
        except KeyboardInterrupt:
            print('[NOTIFICACAO] Worker encerrado.')
            break
        except Exception as e:
            print(f"[NOTIFICACAO] Erro inesperado: {e}. Reiniciando em 5s...")
            time.sleep(5)
