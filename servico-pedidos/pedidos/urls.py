from django.urls import path
from .views import PedidoListCreateView, PedidoDetailView, PedidoPagarView, PedidoCancelarView

urlpatterns = [
    path('pedidos/', PedidoListCreateView.as_view()),
    path('pedidos/<int:pk>/', PedidoDetailView.as_view()),
    path('pedidos/<int:pk>/pagar/', PedidoPagarView.as_view()),
    path('pedidos/<int:pk>/cancelar/', PedidoCancelarView.as_view()),
]
