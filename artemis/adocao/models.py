import uuid
from django.db import models
from django.core.files.storage import default_storage
from django.core.validators import MaxValueValidator
from django.utils import timezone
from datetime import date
from accounts.models import Cliente, Ong

########################### Classes Adoção

class PetPorte(models.Model):
    ptpid = models.AutoField(primary_key=True)
    ptpnome = models.CharField(max_length=100, blank=False, null=False)
    ptpdescricao = models.CharField(max_length=100)

    class Meta:
        db_table = 'pet_porte'

    def __str__(self):
        return self.ptpnome


class PetTipo(models.Model):
    pttid = models.AutoField(primary_key=True)
    pttnome = models.CharField(max_length=60, blank=False, null=False)

    class Meta:
        db_table = 'pet_tipo'

    def __str__(self):
        return self.pttnome


class PetRaca(models.Model):
    ptrid = models.AutoField(primary_key=True)
    ptrnome = models.CharField(max_length=65, blank=False, null=False)
    pet_tipo_pttid = models.ForeignKey(PetTipo, models.DO_NOTHING, db_column='pet_tipo_pttid')

    class Meta:
        db_table = 'pet_raca'

    def __str__(self):
        return self.ptrnome

class Pet(models.Model):
    CASTRADO_CHOICES = [
        ('CAS', 'Castrado'),
        ('NCA', 'Não Castrado'),
        ('DES', 'Desconhecido'),
    ]

    SEXO_CHOICES = [
        ('M', 'Masculino'), 
        ('F', 'Feminino'), 
        ('N', 'Não Informado')
    ]

    petid = models.AutoField(primary_key=True)
    petnome = models.CharField(max_length=100, verbose_name="Nome do Pet", null=False, blank=False)
    petsexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES,
        verbose_name="Sexo do Pet"
    )
    petcastrado = models.CharField(max_length=3, choices=CASTRADO_CHOICES, verbose_name="Status de Castração")
    petdtnascto = models.DateField(
        validators=[MaxValueValidator(timezone.now().date())],
        help_text="A data de nascimento não pode ser futura.",
        verbose_name="Data de Nascimento"
    )
    petpeso = models.FloatField(verbose_name="Peso do Pet")
    cliente_pesid = models.ForeignKey(Cliente, models.CASCADE, db_column='cliente_pesid', blank=True, null=True, verbose_name="Dono do Pet")
    pet_porte_ptpid = models.ForeignKey(PetPorte, models.CASCADE, db_column='pet_porte_ptpid', verbose_name="Porte do Pet")
    pet_raca_ptrid = models.ForeignKey(PetRaca, models.CASCADE, db_column='pet_raca_ptrid', verbose_name="Raça do Pet")
    pet_tipo_pttid = models.ForeignKey(PetTipo, models.CASCADE, db_column='pet_tipo_pttid', verbose_name="Tipo do Pet")

    class Meta:
        db_table = 'pet'
        verbose_name = "Pet"
        verbose_name_plural = "Pets"
    
    def __str__(self):
        return self.petnome

    @property
    def pet_idade(self):
        today = date.today()
        idade = today.year - self.petdtnascto.year
        if today.month < self.petdtnascto.month or (today.month == self.petdtnascto.month and today.day < self.petdtnascto.day):
            idade -= 1
        return idade

class PetAdocao(models.Model):
    ong_ongid = models.ForeignKey(Ong, models.CASCADE, db_column='ong_ongid')
    pet_petid = models.ForeignKey(Pet, models.CASCADE, db_column='pet_petid')
    adoid = models.AutoField(primary_key=True)
    adostatus = models.CharField(max_length=10)

    class Meta:
        db_table = 'pet_adocao'

    def __str__(self):
        return f"{self.ong_ongid.ongnome} - {self.pet_petid.petnome}"


def pet_foto_path(instance, filename):
    ext = filename.split('.')[-1] 
    filename = f"{uuid.uuid4()}.{ext}" 
    return f'adocao/images/pets/{instance.pet_petid.petnome}/{filename}'

class PetFoto(models.Model):
    pftid = models.AutoField(primary_key=True)
    pftfoto = models.ImageField(upload_to=pet_foto_path, max_length=100, verbose_name="Foto do Pet", blank=False, null=False)
    pet_petid = models.ForeignKey(Pet, models.CASCADE, db_column='pet_petid', verbose_name="Pet")

    def delete(self, *args, **kwargs):
        if self.pftfoto and default_storage.exists(self.pftfoto.name):
            self.pftfoto.delete(save=False)
        super().delete(*args, **kwargs)

    class Meta:
        db_table = 'pet_foto'
        verbose_name = "Foto do Pet"
        verbose_name_plural = "Fotos dos Pets"

    def __str__(self):
        return f"{self.pet_petid.petnome} - {self.pftfoto.name if self.pftfoto else 'Sem Foto'}"


class TentativaAdota(models.Model):
    STATUS_CHOICES = [
        ('RE', 'Requisitado'), 
        ('AC', 'Aceito'), 
        ('NE', 'Negado'),
        ('AD', 'Adotado'),
        ('NA', 'Não Adotado')
    ]

    ttaid = models.AutoField(primary_key=True)
    ttapes = models.ForeignKey(Cliente, models.CASCADE, db_column='ttapes', verbose_name="Cliente")
    tta_petadocao = models.ForeignKey(PetAdocao, models.CASCADE, db_column='tta_petadocao', verbose_name="Pet para Adoção")
    ttastatus = models.CharField(max_length=2, choices=STATUS_CHOICES, verbose_name="Status da Tentativa")
    ttadthora = models.DateTimeField(auto_now_add=True, verbose_name="Data e Hora da Tentativa")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data e Hora da Atualização")

    class Meta:
        db_table = 'tentativa_adota'
        verbose_name = "Tentativa de Adoção"
        verbose_name_plural = "Tentativas de Adoção"

    def __str__(self):
        return f"Tentativa de Adoção: {self.ttapes.pesnome} - {self.tta_petadocao.ong_ongid.ongnome} - Status: {self.get_ttastatus_display()}"



