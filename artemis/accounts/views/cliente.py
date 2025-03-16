from rest_framework.viewsets import ModelViewSet
from accounts.serializers import ClienteSerializer
from accounts.models import Cliente

class ClienteViewSet(ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer