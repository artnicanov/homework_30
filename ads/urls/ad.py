from django.urls import path
from ads.views import AdListAll, AdDetailView

urlpatterns = [
    path('', AdListAll.as_view()),
	path('<int:pk>', AdDetailView.as_view())
]