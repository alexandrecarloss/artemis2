from django.db import models

########################### Classes account

class Endereco(models.Model):
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=255)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.logradouro}, {self.bairro} - {self.cidade}/{self.estado}"

class Cliente(models.Model):
    class Sexo(models.TextChoices):
        MASCULINO = "M", 'Masculino'
        FEMININO = "F", 'Feminino'
    
    nome = models.CharField(max_length=100, blank=False, null=False)
    cpf = models.CharField(unique=True, max_length=11)
    dtnascto = models.DateField(blank=False, null=False)
    sexo = models.CharField(max_length=1, choices=Sexo.choices)
    telefone = models.CharField(max_length=15)
    email = models.CharField(unique=True, max_length=70, blank=False, null=False)
    endereco = models.ForeignKey(Endereco, on_delete=models.PROTECT, related_name="clientes")

    def __str__(self):
        return self.nome

class Petshop(models.Model):
    nome = models.CharField(max_length=100, blank=False, null=False)
    cnpj = models.CharField(max_length=20, blank=False, null=False)
    telefone = models.CharField(max_length=15)
    email = models.CharField(unique=True, max_length=70, blank=False, null=False)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, related_name="petshops")

    def __str__(self):
        return self.nome

class Ong(models.Model):
    nome = models.CharField(max_length=65, blank=False, null=False)
    telefone = models.CharField(max_length=15, blank=False, null=False)
    email = models.CharField(max_length=70, blank=False, null=False)
    endereco = models.ForeignKey(Endereco, on_delete=models.PROTECT, related_name="ongs")

    def __str__(self):
        return self.nome
