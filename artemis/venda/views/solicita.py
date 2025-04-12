from rest_framework.viewsets import ModelViewSet
from venda.serializers import  SolicitaSerializer
from venda.models import  Solicita

class  SolicitaViewSet(ModelViewSet):
    queryset =  Solicita.objects.all()
    serializer_class =  SolicitaSerializer