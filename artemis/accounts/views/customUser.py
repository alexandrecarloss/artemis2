from rest_framework.viewsets import ModelViewSet
from accounts.serializers import CustomUserSerializer
from accounts.models import CustomUser

class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer