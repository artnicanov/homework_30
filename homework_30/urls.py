from django.contrib import admin
from django.urls import path, include
from ads.views import root
from rest_framework.routers import SimpleRouter
from users.views import LocationViewSet


router = SimpleRouter()
router.register('location', LocationViewSet)


urlpatterns = [
	path('admin/', admin.site.urls),
	path('', root),
	path('cat/', include('ads.urls.cat')),
	path('ad/', include('ads.urls.ad')),
	path('user/', include('users.users_urls')),
	path('selection/', include('ads.urls.selection')),
]

urlpatterns += router.urls