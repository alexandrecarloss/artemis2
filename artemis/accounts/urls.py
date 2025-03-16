from django.urls import path, include
from rest_framework import routers
from accounts import views as accountsViews

router = routers.DefaultRouter()
router.register(r'enderecos', accountsViews.EnderecoViewSet)
router.register(r'clientes', accountsViews.ClienteViewSet)

urlpatterns = [
    path('accounts/', include(router.urls)),
    path('login/', accountsViews.LoginView.as_view(), name='login'),
]