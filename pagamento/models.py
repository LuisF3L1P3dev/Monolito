from django.db import models

class Transacao(models.Model):
    STATUS_PAGAMENTO = [
        ('PROCESSANDO', 'Processando'),
        ('APROVADO', 'Aprovado'),
        ('RECUSADO', 'Recusado'),
    ]

    # Removido OneToOneField para Pedido para manter isolamento de módulos
    pedido_id = models.PositiveIntegerField(unique=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_PAGAMENTO, default='PROCESSANDO')
    data_transacao = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
       return f"Transação Pedido #{self.pedido_id} - {self.status}"
