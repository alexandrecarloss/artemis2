from django.db import models
from accounts.models import Petshop, Pessoa
from django.core.files.storage import default_storage
import uuid

class CategoriaProduto(models.Model):
    ctpid = models.AutoField(primary_key=True)
    ctpnome = models.CharField(max_length=100)
    ctpdescricao = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'categoria_produto'

    def __str__(self):
        return self.ctpnome


class Produto(models.Model):
    proid = models.AutoField(primary_key=True)
    pronome = models.CharField(max_length=65)
    propreco = models.DecimalField(max_digits=10, decimal_places=2)
    prosaldo = models.PositiveIntegerField(blank=True, null=True)
    propetshop = models.ForeignKey(Petshop, on_delete=models.CASCADE, db_column='propetshop_ptsid')
    procategoria = models.ForeignKey(CategoriaProduto, on_delete=models.CASCADE, db_column='procategoria_produto_ctpid')

    class Meta:
        db_table = 'produto'

    def __str__(self):
        return self.pronome


class TipoServico(models.Model):
    tpsid = models.AutoField(primary_key=True)
    tpsnome = models.CharField(max_length=70)
    tpsdescricao = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'tipo_servico'

    def __str__(self):
        return self.tpsnome


class Servico(models.Model):
    serid = models.AutoField(primary_key=True)
    serdescricao = models.CharField(max_length=200, blank=True, null=True)
    servalor = models.DecimalField(max_digits=10, decimal_places=2)
    serpetshop = models.ForeignKey(Petshop, on_delete=models.CASCADE, db_column='serpetshop_ptsid')
    sertipo = models.ForeignKey(TipoServico, on_delete=models.CASCADE, db_column='sertipo_servico_tpsid')

    class Meta:
        db_table = 'servico'

    def __str__(self):
        return f'Serviço: {self.sertipo.tpsnome} - R$ {self.servalor}'


class Avaliacao(models.Model):
    avaid = models.AutoField(primary_key=True)
    avaproduto = models.ForeignKey(Produto, on_delete=models.CASCADE, blank=True, null=True, db_column='avaproduto_proid')
    avaservico = models.ForeignKey(Servico, on_delete=models.CASCADE, blank=True, null=True, db_column='avaservico_serid')
    avadescricao = models.TextField(blank=True, null=True)
    avavalor = models.PositiveSmallIntegerField()
    avapessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, db_column='avapessoa_pesid')
    avadatahora = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'avaliacao'

    def __str__(self):
        return f'Avaliação {self.avavalor} de {self.avapessoa.pesnome}'


class Favorito(models.Model):
    favid = models.AutoField(primary_key=True)
    favproduto = models.ForeignKey(Produto, on_delete=models.CASCADE, blank=True, null=True, db_column='favproduto_proid')
    favservico = models.ForeignKey(Servico, on_delete=models.CASCADE, blank=True, null=True, db_column='favservico_serid')
    favpessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, db_column='favpessoa_pesid')
    favdatahora = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favorito'
        constraints = [
            models.UniqueConstraint(fields=['favpessoa', 'favproduto'], name='unique_favorito_produto'),
            models.UniqueConstraint(fields=['favpessoa', 'favservico'], name='unique_favorito_servico'),
        ]

    def __str__(self):
        return f'Favorito de {self.favpessoa.pesnome} - {self.favdatahora}'


class Carrinho(models.Model):
    carid = models.AutoField(primary_key=True)
    carproduto = models.ForeignKey(Produto, on_delete=models.CASCADE, blank=True, null=True, db_column='carproduto_proid')
    carservico = models.ForeignKey(Servico, on_delete=models.CASCADE, blank=True, null=True, db_column='carservico_serid')
    carpessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, db_column='carpessoa_pesid')
    carquantidade = models.PositiveIntegerField()
    carprecototal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'carrinho'

    def __str__(self):
        return f'Carrinho de {self.carpessoa.pesnome} - {self.carquantidade}x {self.carproduto.pronome if self.carproduto else self.carservico.serdescricao}'


class FormaPagamento(models.Model):
    fpgid = models.AutoField(primary_key=True)
    fpgdescricao = models.CharField(max_length=65)

    class Meta:
        db_table = 'forma_pagamento'

    def __str__(self):
        return self.fpgdescricao


class Venda(models.Model):
    venid = models.AutoField(primary_key=True)
    venproduto = models.ForeignKey(Produto, on_delete=models.CASCADE, db_column='venproduto_proid')
    venformapagamento = models.ForeignKey(FormaPagamento, on_delete=models.DO_NOTHING, db_column='venformapagamento_fpgid')
    venpessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, db_column='venpessoa_pesid')
    venvalortotal = models.DecimalField(max_digits=10, decimal_places=2)
    vendatahora = models.DateTimeField(auto_now_add=True)
    venquantidade = models.PositiveIntegerField()

    class Meta:
        db_table = 'venda'

    def __str__(self):
        return f'Venda de {self.venquantidade}x {self.venproduto.pronome} para {self.venpessoa.pesnome}'


def produto_foto_path(instance, filename):
    ext = filename.split('.')[-1] 
    filename = f"{uuid.uuid4()}.{ext}" 
    return f'venda/images/produtos/{instance.produto_proid.pronome}/{filename}'

class ProdutoFoto(models.Model):
    prfid = models.AutoField(primary_key=True)
    prffoto = models.ImageField(upload_to=produto_foto_path, max_length=100, verbose_name="Foto do Produto", blank=False, null=False)
    produto_proid = models.ForeignKey(Produto, on_delete=models.CASCADE, db_column='produto_proid', verbose_name="Produto")

    def delete(self, *args, **kwargs):
        if self.prffoto and default_storage.exists(self.prffoto.name):
            self.prffoto.delete(save=False)
        super().delete(*args, **kwargs)

    class Meta:
        db_table = 'produto_foto'
        verbose_name = "Foto do Produto"
        verbose_name_plural = "Fotos dos Produtos"

    def __str__(self):
        return f"{self.produto_proid.pronome} - {self.prffoto.name if self.prffoto else 'Sem Foto'}"

class Solicita(models.Model):
    STATUS_CHOICES = [
        ('RE', 'Requerido'),
        ('CA', 'Cancelado'),
        ('CO', 'Concluído'),
    ]
    
    solid = models.AutoField(primary_key=True)
    pessoa_pesid = models.ForeignKey(Pessoa, models.CASCADE, db_column='pessoa_pesid')
    servico_serid = models.ForeignKey(Servico, models.CASCADE, db_column='servico_serid')
    soldthr = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    solstatus = models.CharField(max_length=2, choices=STATUS_CHOICES)

    class Meta:
        db_table = 'solicita'
        verbose_name = "Solicitação"
        verbose_name_plural = "Solicitações"

    def __str__(self):
        return f'Solicitação {self.solid} - {self.pessoa_pesid.pesnome} - {self.servico_serid.serdescricao}'