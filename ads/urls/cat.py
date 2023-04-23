from rest_framework.routers import SimpleRouter
from ads.views import CatViewSet

router = SimpleRouter()
router.register('', CatViewSet)

urlpatterns = []

urlpatterns += router.urls
