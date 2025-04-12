from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from .models import Cliente, Ong, Petshop, Endereco, CustomUser
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if not username or not password:
            raise serializers.ValidationError("Usuário e senha são obrigatórios.")

        user = authenticate(
            request=self.context.get("request"),
            username=username, 
            password=password
        )

        if not user:
            raise serializers.ValidationError("Usuário e/ou senha incorreto(s)")

        data = super().validate(attrs)

        data["user"] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "tipo": user.tipo,
        }
        return data

# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         user = authenticate(email=data['email'], password=data['password'])
#         if not user:
#             raise serializers.ValidationError("Credenciais inválidas.")
#         data['user'] = user
#         return data
    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "password", "email", "tipo"]
        extra_kwargs = {'password': {'write_only': True}} 

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)
    
# class CustomUserSerializer(ModelSerializer):
#     class Meta:
#         extra_kwargs = {'password': {'write_only': True}}
#         model = CustomUser
#         fields = ["id", "username", "password", "email", "tipo"]

#     def create(self, validated_data):
#         return CustomUser.objects.create_user(
#             email=validated_data["email"],
#             username=validated_data["username"], 
#             password=validated_data["password"], 
#             tipo=validated_data["tipo"]
#         )

class EnderecoSerializer(ModelSerializer):
  class Meta:
    model = Endereco
    fields = ["id", "cep", "logradouro", "bairro", "cidade", "estado", "latitude", "longitude"]

class ClienteSerializer(ModelSerializer):
    endereco = EnderecoSerializer()
    user = serializers.SlugRelatedField(
        queryset=CustomUser.objects.all(), slug_field="username"
    )

    class Meta:
        model = Cliente
        fields = ["user", "nome", "cpf", "dtnascto", "sexo", "telefone", "endereco"]

    def create(self, validated_data):
        user = validated_data.pop("user")
        endereco_data = validated_data.pop("endereco")
        endereco = Endereco.objects.create(**endereco_data)

        cliente = Cliente.objects.create(user=user, endereco=endereco, **validated_data)
        return cliente

class OngSerializer(ModelSerializer):
  endereco = EnderecoSerializer()
  user = serializers.SlugRelatedField(
    queryset=CustomUser.objects.all(), slug_field="username"
    )
  
  class Meta:
    model = Ong
    fields = ["user", "nome", "telefone", "email", "endereco"]

class PetshopSerializer(ModelSerializer):
    endereco = EnderecoSerializer()
    user = serializers.SlugRelatedField(
        queryset=CustomUser.objects.all(), slug_field="username"
    )

    class Meta:
        model = Petshop
        fields = ["user", "nome", "cnpj", "telefone", "endereco"]

    def create(self, validated_data):
        user = validated_data.pop("user")
        endereco_data = validated_data.pop("endereco")
        endereco = Endereco.objects.create(**endereco_data)

        petshop = Petshop.objects.create(user=user, endereco=endereco, **validated_data)
        return petshop