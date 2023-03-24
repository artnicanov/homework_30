from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=40)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True)

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.name


class User(models.Model):
    ROLES = [
        ("member", "Пользователь"),
        ("moderator", "Модератор"),
        ("admin", "Админ"),
    ]

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=9, choices=ROLES, default="member")
    age = models.PositiveIntegerField()
    locations = models.ManyToManyField(Location)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self):
        return self.username


# модели без связи many2many

# class Location(models.Model):
# 	name = models.CharField(max_length=200)
# 	lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
# 	lng = models.DecimalField(max_digits=8, decimal_places=6, null=True)
#
# 	class Meta:
# 		verbose_name = "Место"
# 		verbose_name_plural = "Места"
#
# 	def __str__(self):
# 		return self.name
#
# class User(models.Model):
#
# 	class Roles(models.TextChoices):
# 		ADMIN = 'admin', 'Админ'
# 		MODERATOR = 'moderator', 'Модератор'
# 		MEMBER = 'member', 'Пользователь'
#
# 	first_name = models.CharField(max_length=200)
# 	last_name = models.CharField(max_length=200)
# 	username = models.CharField(max_length=200)
# 	password = models.CharField(max_length=200)
# 	role = models.CharField(max_length=200, choices=Roles.choices)
# 	age = models.PositiveIntegerField()
# 	location = models.ForeignKey(Location, on_delete=models.CASCADE)
#
# 	class Meta:
# 		verbose_name = "Пользователь"
# 		verbose_name_plural = "Пользователи"
#
# 	def __str__(self):
# 		return self.username
