from django.db import models
from cardapio.models import ItemCardapio

# Create your models here.
class Pedido(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
        ('ENVIADO_COZINHA', 'Enviado à Cozinha'),
        ('CANCELADO', 'Cancelado'),]

    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Pedido #{self.id} - {self.status}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    item_cardapio = models.ForeignKey(ItemCardapio, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantidade}x {self.item_cardapio.nome} (Pedido #{self.pedido.id})"