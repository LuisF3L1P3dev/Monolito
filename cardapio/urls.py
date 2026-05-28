from django.urls import path
from .views import (
    ItemCardapioListView, ItemCardapioDetailView, 
    ItemCardapioCreateView, ItemCardapioUpdateView, ItemCardapioDeleteView
)

urlpatterns = [
    path('', ItemCardapioListView.as_view(), name='cardapio-list'),
    path('novo/', ItemCardapioCreateView.as_view(), name='cardapio-create'),
    path('<int:pk>/', ItemCardapioDetailView.as_view(), name='cardapio-detail'),
    path('<int:pk>/editar/', ItemCardapioUpdateView.as_view(), name='cardapio-update'),
    path('<int:pk>/deletar/', ItemCardapioDeleteView.as_view(), name='cardapio-delete'),
]