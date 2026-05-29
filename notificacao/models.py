from django.db import models
from pedidos.models import Pedido

# Create your models here.

class LogNotificacao(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    mensagem = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificação para Pedido #{self.pedido.id} em {self.data_envio}"