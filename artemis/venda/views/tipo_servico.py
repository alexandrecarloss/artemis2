from rest_framework.viewsets import ModelViewSet
from venda.serializers import TipoServicoSerializer
from venda.models import TipoServico

class  TipoServicoViewSet(ModelViewSet):
    queryset =  TipoServico.objects.all()
    serializer_class = TipoServicoSerializer