from rest_framework.viewsets import ModelViewSet
from accounts.serializers import PetshopSerializer
from accounts.models import Petshop

class PetshopViewSet(ModelViewSet):
    queryset = Petshop.objects.all()
    serializer_class = PetshopSerializer