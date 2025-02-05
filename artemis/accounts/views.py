from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import Endereco
from .popular_endereco import buscar_cep

def buscar_endereco(request):
    cep = request.GET.get("cep")
    endereco = Endereco.objects.filter(cep=cep).first()
    if not endereco:
        endereco = salvar_endereco(cep)
    if endereco:
        return JsonResponse({
            "logradouro": endereco.logradouro,
            "bairro": endereco.bairro,
            "cidade": endereco.cidade,
            "estado": endereco.estado
        })
    return JsonResponse({"erro": "CEP não encontrado"}, status=404)
