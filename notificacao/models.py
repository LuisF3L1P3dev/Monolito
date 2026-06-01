from django.db import models

class LogNotificacao(models.Model):
    # Removido ForeignKey direto para Pedido para manter isolamento de módulos
    pedido_id = models.PositiveIntegerField() 
    mensagem = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificação para Pedido #{self.pedido_id} em {self.data_envio}"
