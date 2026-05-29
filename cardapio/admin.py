from django.contrib import admin
from .models import ItemCardapio

@admin.register(ItemCardapio)
class ItemCardapioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'disponivel')
    list_filter = ('disponivel',)
    search_fields = ('nome',)
