from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
########################### Classes account

class Endereco(models.Model):
    logradouro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    cep = models.CharField(max_length=10)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __str__(self):
        return f"{self.logradouro}, {self.bairro} - {self.cidade}/{self.estado}"


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username=username, password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class UserTypes(models.TextChoices):
        CLIENTE = 'cliente', 'Cliente'
        ONG = 'ong', 'ONG'
        PETSHOP = 'petshop', 'Petshop'
    username = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=10, choices=UserTypes.choices)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def is_cliente(self):
        return self.tipo == 'cliente'

    def is_ong(self):
        return self.tipo == 'ong'

    def is_petshop(self):
        return self.tipo == 'petshop' 
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.tipo})"

    
class Cliente(models.Model):
    class Sexo(models.TextChoices):
        MASCULINO = "M", 'Masculino'
        FEMININO = "F", 'Feminino'
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    nome = models.CharField(max_length=100, blank=False, null=False)
    cpf = models.CharField(unique=True, max_length=11)
    dtnascto = models.DateField(blank=False, null=False)
    sexo = models.CharField(max_length=1, choices=Sexo.choices)
    telefone = models.CharField(max_length=15)
    endereco = models.ForeignKey(Endereco, on_delete=models.PROTECT, related_name="clientes")

    def __str__(self):
        return self.nome

class Petshop(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    nome = models.CharField(max_length=100, blank=False, null=False)
    cnpj = models.CharField(max_length=20, blank=False, null=False)
    telefone = models.CharField(max_length=15)
    email = models.CharField(unique=True, max_length=70, blank=False, null=False)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, related_name="petshops")

    def __str__(self):
        return self.nome

class Ong(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    nome = models.CharField(max_length=65, blank=False, null=False)
    telefone = models.CharField(max_length=15, blank=False, null=False)
    email = models.CharField(max_length=70, blank=False, null=False)
    endereco = models.ForeignKey(Endereco, on_delete=models.PROTECT, related_name="ongs")

    def __str__(self):
        return self.nome
