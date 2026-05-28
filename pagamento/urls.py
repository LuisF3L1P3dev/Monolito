from django.urls import path
from .views import ProcessarPagamentoView

urlpatterns = [
    path('processar/<int:pedido_id>/', ProcessarPagamentoView.as_view(), name='processar-pagamento'),
]