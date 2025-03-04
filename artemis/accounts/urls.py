from django.urls import path, include
# from .views import buscar_endereco
from rest_framework import routers
from accounts import views as accountsViews

router = routers.DefaultRouter()
router.register(r'enderecos', accountsViews.EnderecoViewSet)

urlpatterns = [
    path('accounts/', include(router.urls)),
    # path('buscar_endereco/', buscar_endereco, name="buscar_endereco"),
]