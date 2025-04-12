from rest_framework.viewsets import ModelViewSet
from venda.serializers import  ItensCompraSerializer
from venda.models import  ItensCompra

class  ItensCompraViewSet(ModelViewSet):
    queryset =  ItensCompra.objects.all()
    serializer_class =  ItensCompraSerializer