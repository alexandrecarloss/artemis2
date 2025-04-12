from django.db import models
from accounts.models import Petshop, Cliente
from django.core.files.storage import default_storage
import uuid
from django.db.models import F

class CategoriaProduto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=65)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    saldo = models.PositiveIntegerField(blank=True, null=True)
    petshop = models.ForeignKey(Petshop, on_delete=models.PROTECT, related_name='produtos')
    categoria = models.ForeignKey(CategoriaProduto, on_delete=models.PROTECT, related_name='produtos')

    def __str__(self):
        return self.nome


class TipoServico(models.Model):
    nome = models.CharField(max_length=70)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Tipos de Serviço'

    def __str__(self):
        return self.nome


class Servico(models.Model):
    descricao = models.CharField(max_length=200, blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    petshop = models.ForeignKey(Petshop, on_delete=models.PROTECT, related_name='servicos')
    tipo = models.ForeignKey(TipoServico, on_delete=models.PROTECT, related_name='servicos')

    class Meta:
        verbose_name_plural = 'Serviços'

    def __str__(self):
        return f'Serviço: {self.tipo.nome} {self.descricao} - R$ {self.valor}'


class Avaliacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, blank=True, null=True, related_name='avaliacoes')
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, blank=True, null=True, related_name='avaliacoes')
    descricao = models.TextField(blank=True, null=True)
    valor = models.PositiveSmallIntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='avaliacoes')
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cliente', 'produto'], name='unique_avaliacao_produto'),
            models.UniqueConstraint(fields=['cliente', 'servico'], name='unique_avaliacao_servico'),
        ]

    def __str__(self):
        return f'Avaliação {self.valor} de {self.cliente.nome}'


class Favorito(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, blank=True, null=True, related_name='favoritos')
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, blank=True, null=True, related_name='favoritos')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='favoritos')
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cliente', 'produto'], name='unique_favorito_produto'),
            models.UniqueConstraint(fields=['cliente', 'servico'], name='unique_favorito_servico'),
        ]
        

    def __str__(self):
        return f'Favorito de {self.cliente.nome} - {self.criacao}'


class Compra(models.Model):
    class FormaPagamento(models.IntegerChoices):
        CARTAO = 1, 'Cartão'
        PIX = 2, 'Pix'
        BOLETO = 3, 'Boleto'

    class StatusCompra(models.IntegerChoices):
        CARRINHO = 1, 'Carrinho'
        REALIZADO = 2, 'Realizado'
        PAGO = 3, 'Pago'
        ENTREGUE = 4, 'Entregue'
        CANCELADO = 5, 'Cancelado'
        RETORNO = 6, 'Retorno'

    formapagamento = models.IntegerField(choices=FormaPagamento.choices)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='compras')
    status = models.IntegerField(choices=StatusCompra.choices, default=StatusCompra.CARRINHO)
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        queryset = self.itens.all().aggregate(
            total = models.Sum(F('quantidade') * F('produto__preco'))
        )
        return queryset['total'] if queryset else 0.0

    def __str__(self):
        return f'Compra de {self.cliente.nome}'


class ItensCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name="+")
    quantidade = models.IntegerField()


def produto_foto_path(instance, filename):
    ext = filename.split('.')[-1] 
    filename = f"{uuid.uuid4()}.{ext}" 
    return f'venda/images/produtos/{instance.produto.nome}/{filename}'

class ProdutoFoto(models.Model):
    foto = models.ImageField(upload_to=produto_foto_path, max_length=100, blank=False, null=False)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='fotos')

    def delete(self, *args, **kwargs):
        if self.foto and default_storage.exists(self.foto.name):
            self.foto.delete(save=False)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Foto do Produto"
        verbose_name_plural = "Fotos dos Produtos"

    def __str__(self):
        return f"{self.produto.nome} - {self.foto.name if self.foto else 'Sem Foto'}"

class Solicita(models.Model):
    class Status(models.IntegerChoices):
        REQUERIDO = 1, 'Requerido'
        CANCELADO = 2, 'Cancelado'
        CONCLUIDO = 3, 'Concluído'
        REJEITADO = 4, 'Rejeitado'

    cliente = models.ForeignKey(Cliente, models.CASCADE, related_name='solicitacoes')
    servico = models.ForeignKey(Servico, models.CASCADE, related_name='solicitacoes')
    status = models.IntegerField(choices=Status.choices, default=Status.REQUERIDO)
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Solicitação"
        verbose_name_plural = "Solicitações"

    def __str__(self):
        return f'Solicitação de {self.cliente.nome} - {self.servico.descricao}'