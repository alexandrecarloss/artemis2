from rest_framework.viewsets import ModelViewSet
from venda.serializers import  ProdutoFotoSerializer
from venda.models import  ProdutoFoto

class  ProdutoFotoViewSet(ModelViewSet):
    queryset =  ProdutoFoto.objects.all()
    serializer_class =  ProdutoFotoSerializer