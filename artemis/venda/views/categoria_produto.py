from rest_framework.viewsets import ModelViewSet
from venda.serializers import  CategoriaProdutoSerializer
from venda.models import  CategoriaProduto

class  CategoriaProdutoViewSet(ModelViewSet):
    queryset =  CategoriaProduto.objects.all()
    serializer_class =  CategoriaProdutoSerializer