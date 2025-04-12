from rest_framework.viewsets import ModelViewSet
from venda.serializers import  CompraSerializer
from venda.models import  Compra

class  CompraViewSet(ModelViewSet):
    queryset =  Compra.objects.all()
    serializer_class =  CompraSerializer