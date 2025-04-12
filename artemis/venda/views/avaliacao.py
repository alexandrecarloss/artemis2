from rest_framework.viewsets import ModelViewSet
from venda.serializers import  AvaliacaoSerializer
from venda.models import  Avaliacao

class  AvaliacaoViewSet(ModelViewSet):
    queryset =  Avaliacao.objects.all()
    serializer_class =  AvaliacaoSerializer