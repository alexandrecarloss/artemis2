from rest_framework.viewsets import ModelViewSet
from venda.serializers import  FavoritoSerializer
from venda.models import  Favorito

class  FavoritoViewSet(ModelViewSet):
    queryset =  Favorito.objects.all()
    serializer_class =  FavoritoSerializer