from django.urls import path
from .views import ProcessarPagamentoView, StatusPagamentoView

urlpatterns = [
    path('pagamentos/processar/', ProcessarPagamentoView.as_view()),
    path('pagamentos/<int:pedido_id>/status/', StatusPagamentoView.as_view()),
]
