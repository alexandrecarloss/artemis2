from rest_framework.viewsets import ModelViewSet
from accounts.serializers import EnderecoSerializer
from accounts.models import Endereco
# from rest_framework.permissions import IsAuthenticated

class EnderecoViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer