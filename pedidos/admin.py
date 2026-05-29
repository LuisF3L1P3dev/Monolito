import time
from django.contrib import admin
from django.contrib import messages
from .models import Pedido, ItemPedido
from pagamento.models import Transacao
from notificacao.services import notificar_cozinha

@admin.action(description="Processar Pagamento (Simular fluxo completo)")
def processar_pagamento_action(modeladmin, request, queryset):
    for pedido in queryset:
        if pedido.status != 'PENDENTE':
            modeladmin.message_user(request, f"O Pedido #{pedido.id} não está PENDENTE. Status atual: {pedido.status}", level=messages.WARNING)
            continue

        # 1. Cria a Transação
        transacao, _ = Transacao.objects.get_or_create(pedido=pedido)
        
        # 2. Simula latência
        time.sleep(5)
        
        # 3. Aprova Transação e atualiza Pedido
        transacao.status = 'APROVADO'
        transacao.save()
        
        pedido.status = 'PAGO'
        pedido.save(update_fields=['status'])
        
        # 4. Chama serviço de notificação
        notificar_cozinha(pedido.id)
        
        modeladmin.message_user(request, f"Pagamento do Pedido #{pedido.id} processado. Enviado para a cozinha!", level=messages.SUCCESS)

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
    list_display = ('pedido', 'item_cardapio', 'quantidade')
