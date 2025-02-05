from django.contrib import admin
from django.urls import path
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('venda/', include('venda.urls')),
    path('adocao/', include('adocao.urls')),
    path('accounts/', include('accounts.urls')),
]
