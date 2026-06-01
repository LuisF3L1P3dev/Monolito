from django.contrib import admin
from .models import LogNotificacao

@admin.register(LogNotificacao)
class LogNotificacaoAdmin(admin.ModelAdmin):
    list_display = ('pedido_id', 'data_envio')
    readonly_fields = ('pedido_id', 'mensagem', 'data_envio')
