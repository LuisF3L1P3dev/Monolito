from django.contrib import admin
from .models import LogNotificacao

@admin.register(LogNotificacao)
class LogNotificacaoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'data_envio')
    readonly_fields = ('pedido', 'mensagem', 'data_envio')
