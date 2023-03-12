import json
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from ads.models import Category, Ad
from users.models import User

def root(request):
	return JsonResponse({"status": "ok"})


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

############# CRUD ДЛЯ КАТЕГОРИЙ ###############

# вьюшка для вывода списка категорий
class CategoryListView(generic.ListView):
	model = Category
	queryset = Category.objects.all()

	def get(self, request, *args, **kwargs):
		categories = self.queryset.order_by('name')  # сортировка категорий по алфавиту
		categories_list = serialize(Category, categories)
		return JsonResponse(categories_list, safe=False)


# вьюшка для вывода категории по id
class CategoryDetailView(generic.DetailView):
	model = Category

	def get(self, request, *args, **kwargs):
		try:
			category = Category.objects.get(pk=kwargs['pk'])
		except Category.DoesNotExist as e:
			return JsonResponse({'detail': "Категория не найдена"}, status=404)
		res = serialize(Category, category)
		return JsonResponse(res, safe=False)


# вьюшка для создания новой категории
@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(generic.CreateView):
	model = Category
	fields = ['name']

	def post(self, request, *args, **kwargs):
		data = json.loads(request.body)
		category = Category.objects.create(**data)
		result = serialize(Category, category)
		return JsonResponse(result, safe=False)


# вьюшка для изменения категории по id
@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(generic.UpdateView):
	model = Category
	fields = ['name']

	def patch(self, request, *args, **kwargs):
		data = json.loads(request.body)
		category = Category.objects.get(id=kwargs['pk'])
		category.name = data['name']
		category.save()
		result = serialize(Category, category)
		return JsonResponse(result, safe=False)

# вьюшка для удаления категории по id
@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(generic.DeleteView):
	model = Category
	success_url = '/'

	def delete(self, request, *args, **kwargs):
		super().delete(request, *args, **kwargs)
		return JsonResponse({'status': 'ok'}, status=200)


############# CRUD ДЛЯ ОБЪЯВЛЕНИЙ ###############

# вьюшка для вывода списка объявлений
class AdListView(generic.ListView):
	model = Ad
	queryset = Ad.objects.all()

	def get(self, request, *args, **kwargs):
		super().get(request, *args, **kwargs)
		self.object_list = self.object_list.select_related('author_id').order_by('-price')  # сортировка объявлений по убыванию цены
		paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		ads = serialize(Ad, page_obj)

		response = {
			"items": ads,
			"num_pages": page_obj.paginator.num_pages,
			"total": page_obj.paginator.count
		}

		return JsonResponse(response, safe=False)


# вьюшка для вывода объявления по id
class AdDetailView(generic.DetailView):
	model = Ad

	def get(self, request, *args, **kwargs):
		try:
			ad = Ad.objects.get(pk=kwargs['pk'])
		except Ad.DoesNotExist as e:
			return JsonResponse({'detail': "Объявление не найдено"}, status=404)
		result = serialize(Ad, ad)

		return JsonResponse(result, safe=False)

# вьюшка для создания нового объявления, работает только через админку, через постман пока нет, доделать
@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(generic.CreateView):
	model = Ad
	fields = ['username']

	def post(self, request, *args, **kwargs):
		data = json.loads(request.body)
		ad = Ad.objects.create(**data)
		result = serialize(Ad, ad)
		return JsonResponse(result, safe=False)

# вьюшка для изменения объявления по id
@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(generic.UpdateView):
	model = Ad
	fields = ['description']

	def patch(self, request, *args, **kwargs):
		data = json.loads(request.body)
		ad = Ad.objects.get(id=kwargs['pk'])
		ad.name = data['name']
		ad.description = data['description']
		ad.price = data['price']
		ad.save()
		result = serialize(Ad, ad)
		return JsonResponse(result, safe=False)

# вьюшка для удаления объявления по id
@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(generic.DeleteView):
	model = Ad
	success_url = '/'

	def delete(self, request, *args, **kwargs):
		super().delete(request, *args, **kwargs)
		return JsonResponse({'status': 'ok'}, status=200)

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


############# CRUD ДЛЯ ПОЛЬЗОВАТЕЛЕЙ ###############

# вьюшка для вывода списка пользователей
class UserListView(generic.ListView):
	model = User
	queryset = User.objects.all()

	def get(self, request, *args, **kwargs):
		super().get(request, *args, **kwargs)
		self.object_list = self.queryset.order_by('username')  # сортировка пользователей по алфавиту
		users = serialize(User, self.object_list)

		response = {
			"items": users
		}
		return JsonResponse(response, safe=False)


# вьюшка для вывода пользователя по id
class UserDetailView(generic.DetailView):
	model = User

	def get(self, request, *args, **kwargs):
		try:
			user = User.objects.get(pk=kwargs['pk'])
		except User.DoesNotExist as e:
			return JsonResponse({'detail': "Пользователь не найден"}, status=404)
		result = serialize(User, user)

		return JsonResponse(result, safe=False)

# вьюшка для создания нового пользователя, работает только через админку, через постман пока нет, доделать
@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(generic.CreateView):
	model = User
	fields = ['username']

	def post(self, request, *args, **kwargs):
		data = json.loads(request.body)
		user = User.objects.create(**data)
		result = serialize(User, user)
		return JsonResponse(result, safe=False)

# вьюшка для изменения пользователя по id
@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(generic.UpdateView):
	model = User

	def patch(self, request, *args, **kwargs):
		data = json.loads(request.body)
		user = User.objects.get(id=kwargs['pk'])
		user.password = data['password']
		user.save()
		result = serialize(User, user)
		return JsonResponse(result, safe=False)

# вьюшка для удаления пользователя по id
@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(generic.DeleteView):
	model = User
	success_url = '/'

	def delete(self, request, *args, **kwargs):
		super().delete(request, *args, **kwargs)
		return JsonResponse({'status': 'ok'}, status=200)
