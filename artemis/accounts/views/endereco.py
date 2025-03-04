from rest_framework.viewsets import ModelViewSet
from accounts.serializers import EnderecoSerializer
from accounts.models import Endereco

class EnderecoViewSet(ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer