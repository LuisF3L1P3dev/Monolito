from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Pedido

class PedidoListView(ListView):
    model = Pedido
    # Procura por: pedidos/pedido_list.html

class PedidoDetailView(DetailView):
    model = Pedido
    # Procura por: pedidos/pedido_detail.html

class PedidoCreateView(CreateView):
    model = Pedido
    fields = ['status', 'total'] # Ajuste caso queira tratar os ItensPedido depois
    success_url = reverse_lazy('pedidos-list')
    # Procura por: pedidos/pedido_form.html

class PedidoUpdateView(UpdateView):
    model = Pedido
    fields = ['status', 'total']
    success_url = reverse_lazy('pedidos-list')
    # Procura por: pedidos/pedido_form.html

class PedidoDeleteView(DeleteView):
    model = Pedido
    success_url = reverse_lazy('pedidos-list')
    # Procura por: pedidos/pedido_confirm_delete.html