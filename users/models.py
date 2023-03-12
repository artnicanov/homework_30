from django.db import models

# Create your models here.

class Location(models.Model):
	name = models.CharField(max_length=200)
	lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
	lng = models.DecimalField(max_digits=8, decimal_places=6, null=True)

	class Meta:
		verbose_name = "Место"
		verbose_name_plural = "Места"

	def __str__(self):
		return self.name

class User(models.Model):

	class Roles(models.TextChoices):
		ADMIN = 'admin', 'Админ'
		MODERATOR = 'moderator', 'Модератор'
		MEMBER = 'member', 'Пользователь'

	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	role = models.CharField(max_length=200, choices=Roles.choices)
	age = models.PositiveIntegerField()
	location = models.ForeignKey(Location, on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Пользователь"
		verbose_name_plural = "Пользователи"

	def __str__(self):
		return self.username
