import json
import pika
from django.conf import settings


def publicar_notificacao_fila(pedido_id: int, mensagem: str) -> None:
    """
    Publica mensagem na fila RabbitMQ para o servico-notificacao consumir.
    Se a fila estiver indisponível, registra o erro mas NÃO falha o pagamento
    (resiliência: desacoplamento via mensageria assíncrona).
    """
    try:
        params = pika.URLParameters(settings.RABBITMQ_URL)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        channel.queue_declare(queue='notificacao_cozinha', durable=True)
        channel.basic_publish(
            exchange='',
            routing_key='notificacao_cozinha',
            body=json.dumps({'pedido_id': pedido_id, 'mensagem': mensagem}),
            properties=pika.BasicProperties(delivery_mode=2),  # mensagem persistente
        )
        connection.close()
        print(f"[PAGAMENTO] Notificação enfileirada para pedido #{pedido_id}")
    except Exception as e:
        # Pagamento não falha se a fila estiver indisponível
        print(f"[PAGAMENTO] AVISO: Fila indisponível — pedido #{pedido_id} pago mas notificação não enviada: {e}")
