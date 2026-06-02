from django.urls import path
from .views import ItemCardapioListCreateView, ItemCardapioDetailView

urlpatterns = [
    path('cardapio/', ItemCardapioListCreateView.as_view()),
    path('cardapio/<int:pk>/', ItemCardapioDetailView.as_view()),
]
