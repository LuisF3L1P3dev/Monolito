from django.contrib import admin
from django.contrib import messages
from .models import Pedido, ItemPedido
from pagamento.services import PagamentoPadraoService
from notificacao.services import NotificacaoService

@admin.action(description="Processar Pagamento (Via Services Modular)")
def processar_pagamento_action(modeladmin, request, queryset):
    for pedido in queryset:
        if pedido.status != 'PENDENTE':
            modeladmin.message_user(request, f"O Pedido #{pedido.id} não está PENDENTE. Status atual: {pedido.status}", level=messages.WARNING)
            continue

        # Uso dos Services para manter o isolamento modular
        pagamento_service = PagamentoPadraoService()
        sucesso = pagamento_service.processar_pagamento(pedido.id, pedido.total)
        
        if sucesso:
            NotificacaoService.notificar_cozinha(pedido.id)
            modeladmin.message_user(request, f"Pagamento do Pedido #{pedido.id} processado via Service. Enviado para a cozinha!", level=messages.SUCCESS)
        else:
            modeladmin.message_user(request, f"Falha ao processar pagamento do Pedido #{pedido.id}", level=messages.ERROR)

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_criacao', 'status', 'total')
    list_filter = ('status', 'data_criacao')
    inlines = [ItemPedidoInline]
    actions = [processar_pagamento_action]

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'item_cardapio_id', 'quantidade')
