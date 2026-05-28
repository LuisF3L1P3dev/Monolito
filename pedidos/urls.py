from django.urls import path
from .views import (
    PedidoListView, PedidoDetailView, 
    PedidoCreateView, PedidoUpdateView, PedidoDeleteView
)

urlpatterns = [
    path('', PedidoListView.as_view(), name='pedidos-list'),
    path('novo/', PedidoCreateView.as_view(), name='pedidos-create'),
    path('<int:pk>/', PedidoDetailView.as_view(), name='pedidos-detail'),
    path('<int:pk>/editar/', PedidoUpdateView.as_view(), name='pedidos-update'),
    path('<int:pk>/deletar/', PedidoDeleteView.as_view(), name='pedidos-delete'),
]