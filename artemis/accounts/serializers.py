from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from .models import Cliente, Ong, Petshop, Endereco
from rest_framework import serializers

class EnderecoSerializer(ModelSerializer):
  class Meta:
    model = Endereco
    fields = ["id", "cep", "logradouro", "bairro", "cidade", "estado"]

class CriarEditarClienteSerializer(ModelSerializer):
  class Meta:
    model = Cliente
    fields = ["nome", "cpf", "dtnascto", "sexo", "telefone", "email", "endereco"]

class ClienteDetailSerializer(ModelSerializer):
  class Meta:
    model = Cliente
    fields = ["id", "nome", "cpf", "dtnascto", "sexo", "telefone", "email", "endereco"]
  