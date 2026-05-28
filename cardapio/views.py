from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import ItemCardapio

class ItemCardapioListView(ListView):
    model = ItemCardapio
    # Procura por: cardapio/itemcardapio_list.html

class ItemCardapioDetailView(DetailView):
    model = ItemCardapio
    # Procura por: cardapio/itemcardapio_detail.html

class ItemCardapioCreateView(CreateView):
    model = ItemCardapio
    fields = ['nome', 'descricao', 'preco', 'disponivel']
    success_url = reverse_lazy('cardapio-list')
    # Procura por: cardapio/itemcardapio_form.html

class ItemCardapioUpdateView(UpdateView):
    model = ItemCardapio
    fields = ['nome', 'descricao', 'preco', 'disponivel']
    success_url = reverse_lazy('cardapio-list')
    # Procura por: cardapio/itemcardapio_form.html

class ItemCardapioDeleteView(DeleteView):
    model = ItemCardapio
    success_url = reverse_lazy('cardapio-list')
    # Procura por: cardapio/itemcardapio_confirm_delete.html