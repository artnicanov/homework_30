from django.urls import path
from rest_framework.routers import SimpleRouter

from ads import views
from ads.views import AdViewSet

router = SimpleRouter()
router.register('', AdViewSet)

urlpatterns = [
	path('<int:pk>/upload_image/', views.AdUploadImageView.as_view(), name='ad_upload_image'),
]

urlpatterns += router.urls