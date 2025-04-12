from rest_framework.serializers import ModelSerializer
from venda.models import CategoriaProduto, Produto, Servico, Avaliacao, Favorito, Compra, ItensCompra, ProdutoFoto, Solicita
from accounts.models import Petshop, Cliente
from rest_framework import serializers

class CategoriaProdutoSerializer(ModelSerializer):
  class Meta:
    model = CategoriaProduto
    fields = ["id", "nome", "descricao"]
    read_only_fields = ["id"]

class ProdutoSerializer(serializers.ModelSerializer):
    petshop = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Produto
        fields = ["id", "nome", "preco", "saldo", "petshop", "categoria"]
        read_only_fields = ["id", "petshop"]

    def validate_petshop(self, value):
        user = self.context["request"].user 

        if not hasattr(user, 'petshop'):
            raise serializers.ValidationError("Apenas usuários do tipo Petshop podem adicionar produtos.")
        
        return user.petshop
    
# class ProdutoSerializer(ModelSerializer):
#   petshop = serializers.HiddenField(default=serializers.CurrentUserDefault())
#   class Meta:
#     model = Produto
#     fields = ["id", "nome", "preco", "saldo", "petshop", "categoria"]
#     read_only_fields = ["id", "petshop"]

class TipoServicoSerializer(ModelSerializer):
  class Meta:
    model = CategoriaProduto
    fields = ["id", "nome", "descricao"]
    read_only_fields = ["id"]


class ServicoSerializer(ModelSerializer):
  petshop = serializers.HiddenField(default=serializers.CurrentUserDefault())
  # petshop = Petshop.objects.get(user=usuario)

  class Meta: 
    model = Servico
    fields = ["id", "descricao", "petshop", "valor", "tipo"]
    read_only_fields = ["id"]

class AvaliacaoSerializer(ModelSerializer):
  # cliente = serializers.HiddenField(default=serializers.CurrentUserDefault())

  class Meta:
    model = Avaliacao
    fields = ["id", "produto", "servico", "descricao", "valor", "cliente", "criacao", "atualizacao"]
    read_only_fields = ["id", "criacao", "atualizacao"]

class FavoritoSerializer(ModelSerializer):
  # cliente = serializers.HiddenField(default=serializers.CurrentUserDefault())

  class Meta:
    model = Favorito
    fields = ["id", "produto", "servico", "cliente", "criacao", "atualizacao"]
    read_only_fields = ["id", "criacao", "atualizacao"]

class CompraSerializer(ModelSerializer):
  # cliente = serializers.HiddenField(default=serializers.CurrentUserDefault())

  class Meta:
    model = Compra
    fields = ["id", "formapagamento", "cliente", "status", "criacao", "atualizacao"]
    read_only_fields = ["id", "criacao", "atualizacao"]

class ItensCompraSerializer(ModelSerializer):

  class Meta:
    model = ItensCompra
    fields = ["id", "compra", "produto", "quantidade"]
    read_only_fields = ["id"]

class ProdutoFotoSerializer(ModelSerializer):

  class Meta:
    model = ProdutoFoto
    fields = ["id", "foto", "produto"]
    read_only_fields = ["id"]

class SolicitaSerializer(ModelSerializer):
  # cliente = serializers.HiddenField(default=serializers.CurrentUserDefault())

  class Meta:
    model = Solicita
    fields = ["id", "cliente", "servico", "status", "criacao", "atualizacao"]
    read_only_fields = ["id", "criacao", "atualizacao"]
