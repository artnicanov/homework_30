from django.contrib import admin
from django.urls import path, include
from ads.views import root

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', root),
	path('cat/', include('ads.urls.cat')),
	path('ad/', include('ads.urls.ad')),
	path('users/', include('users.users_urls')),

]
