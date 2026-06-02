from django.db import models

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
        ('ENVIADO_COZINHA', 'Enviado à Cozinha'),
        ('CANCELADO', 'Cancelado'),
    ]

    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.status}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    item_cardapio_id = models.PositiveIntegerField()
    nome_item = models.CharField(max_length=255)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.nome_item} x{self.quantidade} (Pedido #{self.pedido.id})"
