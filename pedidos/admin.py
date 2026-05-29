from django.contrib import admin
from .models import Pedido, ItemPedido

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_criacao', 'status', 'total')
    list_filter = ('status', 'data_criacao')
    inlines = [ItemPedidoInline]

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'item_cardapio', 'quantidade')
