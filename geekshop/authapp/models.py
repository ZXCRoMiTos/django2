from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta


class ShopUser(AbstractUser):
    age = models.PositiveIntegerField('возраст', null=True)
    avatar = models.ImageField(upload_to='avatars', blank=True)
    is_activate = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=now() + timedelta(hours=48))

    def basket_price(self):
        return sum(el.product_cost for el in self.basket.all())

    def basket_qty(self):
        return sum(el.qty for el in self.basket.all())

    def is_valid_key(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True
