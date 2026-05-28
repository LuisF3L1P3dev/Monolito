from django.db import models

# Create your models here.
class ItemCardapio(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    disponivel = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"