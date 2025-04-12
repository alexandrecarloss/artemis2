from django.urls import path, include
from venda import views as vendasViews

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'categorias_produto', vendasViews.CategoriaProdutoViewSet)
router.register(r'produtos', vendasViews.ProdutoViewSet)
router.register(r'servicos', vendasViews.ServicoViewSet)
router.register(r'tipos_servico', vendasViews.TipoServicoViewSet)
router.register(r'avaliacao', vendasViews.AvaliacaoViewSet)
router.register(r'favorito', vendasViews.FavoritoViewSet)
router.register(r'compra', vendasViews.CompraViewSet)
router.register(r'itens_compra', vendasViews.ItensCompraViewSet)
router.register(r'produto_foto', vendasViews.ProdutoFotoViewSet)
router.register(r'solicita', vendasViews.SolicitaViewSet)


urlpatterns = [
    path('/', include(router.urls)),
]