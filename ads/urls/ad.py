from django.urls import path
from ads import views

urlpatterns = [
	path('', views.AdListView.as_view(), name='ad_list'),
	path('create/', views.AdCreateView.as_view(), name='ad_create'),
	path('<int:pk>', views.AdDetailView.as_view(), name='ad_detail'),
	path('<int:pk>/update/', views.AdUpdateView.as_view(), name='ad_update'),
	path('<int:pk>/upload_image/', views.AdUploadImageView.as_view(), name='ad_upload_image'),
	path('<int:pk>/delete/', views.AdDeleteView.as_view(), name='ad_delete')
]
