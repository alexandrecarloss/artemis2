# import requests
# from core.models import Endereco

# def buscar_cep(cep):
#     url = f"https://viacep.com.br/ws/{cep}/json/"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()
#     return None

# def salvar_endereco(cep):
#     dados = buscar_cep(cep)
#     if dados and "erro" not in dados:
#         endereco, created = Endereco.objects.get_or_create(
#             cep=cep,
#             defaults={
#                 "logradouro": dados["logradouro"],
#                 "bairro": dados["bairro"],
#                 "cidade": dados["localidade"],
#                 "estado": dados["uf"]
#             }
#         )
#         return endereco
#     return None
