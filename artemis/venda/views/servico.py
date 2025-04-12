from rest_framework.viewsets import ModelViewSet
from venda.serializers import ServicoSerializer
from venda.models import Servico

class  ServicoViewSet(ModelViewSet):
    queryset =  Servico.objects.all()
    serializer_class = ServicoSerializer