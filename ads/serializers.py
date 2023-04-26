from rest_framework.serializers import ModelSerializer

from ads.models import Ad, Category, Selection


class AdSerializer(ModelSerializer):
	class Meta:
		model = Ad
		fields = '__all__'


class CatSerializer(ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'


class SelectionSerializer(ModelSerializer):
	class Meta:
		model = Selection
		fields = '__all__'