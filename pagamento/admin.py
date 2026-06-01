from django.contrib import admin
from .models import Transacao

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('pedido_id', 'valor', 'status', 'data_transacao')
    list_filter = ('status',)
