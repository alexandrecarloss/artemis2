from django.urls import path, include
from accounts import views as accountsViews

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'enderecos', accountsViews.EnderecoViewSet)
router.register(r'clientes', accountsViews.ClienteViewSet)
router.register(r'customUsers', accountsViews.CustomUserViewSet)
router.register(r'petshops', accountsViews.PetshopViewSet)

urlpatterns = [
    path('/', include(router.urls)),
    # path('login/', accountsViews.LoginView.as_view(), name='login'),
]