from django.db import models

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

    def calcular_total(self):
        # Soma o valor de todos os itens usando o preço capturado no momento da criação
        novo_total = sum(item.preco_unitario * item.quantidade for item in self.itens.all())
        self.total = novo_total
        self.save(update_fields=['total'])

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    item_cardapio_id = models.PositiveIntegerField() # Desacoplado do model ItemCardapio
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # Snapshot do preço
    
    def __str__(self):
        return f"Item {self.item_cardapio_id} (Pedido #{self.pedido.id})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.pedido.calcular_total()

    def delete(self, *args, **kwargs):
        pedido = self.pedido
        super().delete(*args, **kwargs)
        pedido.calcular_total()
