from django.contrib import admin
from django.urls import path, include
from accounts import urls as accountsUrls
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from accounts import views as accountsViews
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Open API3
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # Autenticação
    path("token/", accountsViews.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('admin/', admin.site.urls),
    # Endpoints
    path('api/', include(accountsUrls))
    # path('venda/', include('venda.urls')),
    # path('adocao/', include('adocao.urls')),
    # path('accounts/', include('accounts.urls')),
]
