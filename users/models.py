from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import TextChoices


class Location(models.Model):
    name = models.CharField(max_length=40)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True)

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.name


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "admin", "Админ"
        MODERATOR = "moderator", "Модератор"
        MEMBER = "member", "Пользователь"

    role = models.CharField(max_length=25, choices=Roles.choices, default=Roles.MEMBER)
    age = models.PositiveIntegerField(null=True)
    location = models.ManyToManyField(Location)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self):
        return self.username
