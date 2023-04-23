from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from ads.models import Category, Ad
from ads.serializers import AdSerializer, CatSerializer
from rest_framework.viewsets import ModelViewSet


def root(request):
	return JsonResponse({"status": "ok"})


# сериализатор для обработки файла с картинкой объявления
def serialize(model, values):
	if isinstance(values, model):
		values = [values]
	else:
		list(values)
	result = []
	for value in values:
		data = {}
		for field in model._meta.get_fields():
			if field.is_relation:
				continue
			if field.name == 'image':
				data[field.name] = getattr(value.image, 'url', None)
			else:
				data[field.name] = getattr(value, field.name)
		result.append(data)
	return result


# CRUD для категорий в одной DRF вьюшке
class CatViewSet(ModelViewSet):
	serializer_class = CatSerializer
	queryset = Category.objects.all()

# CRUD для объявлений в одной DRF вьюшке
class AdViewSet(ModelViewSet):
	serializer_class = AdSerializer
	queryset = Ad.objects.order_by('-price')


	# функции с lookup's для поисковых фильтров
	def list(self, request, *args, **kwargs):

		# поиск категорий
		categories = request.GET.getlist('cat')
		if categories:
			self.queryset = self.queryset.filter(category_id__in=categories)

		# поиск объявлений по словам в названии без учета регистра
		text = request.GET.get('text')
		if text:
			self.queryset = self.queryset.filter(name__icontains=text)

		# поиск по адресу автора без учета регистра
		location = request.GET.get('location')
		if location:
			self.queryset = self.queryset.filter(author__locations__name__icontains=location)

		# поиск по цене равной или выше
		price_from = request.GET.get('price_from')
		if price_from:
			self.queryset = self.queryset.filter(price__gte=price_from)

		# поиск по цене равной или ниже
		price_to = request.GET.get('price_to')
		if price_to:
			self.queryset = self.queryset.filter(price__lte=price_to)

		return super().list(request, *args, **kwargs)

# вьюшка для добавления картнинки к объявлению
@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImageView(generic.UpdateView):
	model = Ad
	fields = ['image']

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.image = request.FILES.get('image')
		self.object.save()

		result = serialize(self.model, self.object)
		return JsonResponse(result, safe=False)
