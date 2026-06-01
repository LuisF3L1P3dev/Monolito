from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import ItemCardapio
from .serializers import ItemCardapioSerializer

class ItemCardapioListCreateView(generics.ListCreateAPIView):
    queryset = ItemCardapio.objects.all()
    serializer_class = ItemCardapioSerializer

class ItemCardapioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ItemCardapio.objects.all()
    serializer_class = ItemCardapioSerializer
