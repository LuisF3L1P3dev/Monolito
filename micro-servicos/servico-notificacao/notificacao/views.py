from rest_framework import generics
from .models import LogNotificacao
from .serializers import LogNotificacaoSerializer


class LogNotificacaoListCreateView(generics.ListCreateAPIView):
    queryset = LogNotificacao.objects.order_by('-data_envio')
    serializer_class = LogNotificacaoSerializer
