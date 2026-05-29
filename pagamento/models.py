from django.db import models
from pedidos.models import Pedido
# Create your models here.
class Transacao(models.Model):
    STATUS_PAGAMENTO = [
        ('PROCESSANDO', 'Processando'),
        ('APROVADO', 'Aprovado'),
        ('RECUSADO', 'Recusado'),]

    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='transacao')
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_PAGAMENTO, default='PROCESSANDO')
    data_transacao = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
       return f"Transação Pedido #{self.pedido.id} - {self.status}"

    def save(self, *args, **kwargs):
        # Sincroniza o valor da transação com o total atual do pedido caso não tenha sido informado
        if self.pedido and not self.valor:
            self.valor = self.pedido.total
        super().save(*args, **kwargs)