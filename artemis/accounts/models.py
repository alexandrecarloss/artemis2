from django.db import models

########################### Classes account

class Endereco(models.Model):
    endid = models.AutoField(primary_key=True)
    endcep = models.CharField(max_length=9)
    endlogradouro = models.CharField(max_length=255)
    endbairro = models.CharField(max_length=100)
    endcidade = models.CharField(max_length=100)
    endestado = models.CharField(max_length=2)

    class Meta:
        db_table = 'endereco'

    def __str__(self):
        return f"{self.logradouro}, {self.bairro} - {self.cidade}/{self.estado}"

class Pessoa(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]
    pesid = models.AutoField(primary_key=True)
    pescpf = models.CharField(unique=True, max_length=11)
    pesdtnascto = models.DateField(blank=False, null=False)
    pessexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    pesemail = models.CharField(unique=True, max_length=70, blank=False, null=False)
    pestelefone = models.CharField(max_length=15)
    pesnome = models.CharField(max_length=100, blank=False, null=False)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, db_column='endereco_endid')

    class Meta:
        db_table = 'pessoa'

    def __str__(self):
        return self.pesnome

class Petshop(models.Model):
    ptsid = models.AutoField(primary_key=True)
    ptsnome = models.CharField(max_length=100, blank=False, null=False)
    ptscnpj = models.CharField(max_length=20, blank=False, null=False)
    ptstelefone = models.CharField(max_length=15)
    ptsemail = models.CharField(unique=True, max_length=70, blank=False, null=False)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, db_column='ptsendereco_endid')

    class Meta:
        db_table = 'petshop'

    def __str__(self):
        return self.ptsnome

class Ong(models.Model):
    ongid = models.AutoField(primary_key=True)
    ongnome = models.CharField(max_length=65, blank=False, null=False)
    ongtelefone = models.CharField(max_length=15, blank=False, null=False)
    ongemail = models.CharField(max_length=70, blank=False, null=False)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, db_column='ongendereco_endid')

    class Meta:
        db_table = 'ong'

    def __str__(self):
        return self.ongnome
