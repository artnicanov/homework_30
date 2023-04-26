from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import User, Location
from users.serializers import UserSerializer, UserListSerializer, UserDetailSerializer, LocationSerializer, \
	UseCreateSerializer


class UserPagination(PageNumberPagination):
	page_size = 4


# CRUD для пользователей с generic views
class UserCreateView(CreateAPIView):
	serializer_class = UseCreateSerializer
	queryset = User.objects.all()


class UserDetailView(RetrieveAPIView):
	serializer_class = UserDetailSerializer
	queryset = User.objects.all()


class UserDeleteView(DestroyAPIView):
	serializer_class = UserSerializer
	queryset = User.objects.all()


class UserListView(ListAPIView):
	serializer_class = UserListSerializer
	queryset = User.objects.order_by('username')
	pagination_class = UserPagination


class UserUpdateView(UpdateAPIView):
	serializer_class = UserSerializer
	queryset = User.objects.all()


# CRUD для адресов в одной DRF вьюшке
class LocationViewSet(ModelViewSet):
	serializer_class = LocationSerializer
	queryset = Location.objects.all()