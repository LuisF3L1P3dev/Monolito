from django.urls import path
from .views import LogNotificacaoListCreateView

urlpatterns = [
    path('notificacoes/', LogNotificacaoListCreateView.as_view()),
]
