from rest_framework.viewsets import ModelViewSet
from venda.serializers import ProdutoSerializer
from venda.models import Produto
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

class ProdutoViewSet(ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # def perform_create(self, serializer):
    #     user = self.request.user
    #     if not hasattr(user, 'petshop'):
    #         return Response(
    #             {"error": "Apenas usuários do tipo Petshop podem adicionar produtos."},
    #             status=status.HTTP_403_FORBIDDEN
    #         )
    #     serializer.save(petshop=user.petshop)
