from django.urls import path
from ads.views import CategoryDetailView, CatListAll

urlpatterns = [
    path('', CatListAll.as_view()),
	path('<int:pk>', CategoryDetailView.as_view())
]