from django.contrib import admin
from django.urls import path, include
from accounts import urls as accountsUrls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(accountsUrls))
    # path('venda/', include('venda.urls')),
    # path('adocao/', include('adocao.urls')),
    # path('accounts/', include('accounts.urls')),
]
