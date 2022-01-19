from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from geekshop.settings import ACTIVATION_KEY_TTL


class ShopUser(AbstractUser):
    age = models.PositiveIntegerField('возраст', null=True)
    avatar = models.ImageField(upload_to='avatars', blank=True)
    is_activate = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=128, blank=True)

    def basket_price(self):
        return sum(el.product_cost for el in self.basket.all())

    def basket_qty(self):
        return sum(el.qty for el in self.basket.all())

    def is_valid_key(self):
        return now() - self.date_joined > timedelta(hours=ACTIVATION_KEY_TTL)

    def send_verify_mail(self):
        verify_link = reverse('auth:verify', args=[self.email, self.activation_key])
        title = f'Подтверждение учетной записи {self.username}'
        message = f'Для подтверждения учетной записи {self.username} на портале ' \
                  f'{settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

        return send_mail(title, message, settings.EMAIL_HOST_USER, [self.email], fail_silently=False)


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOISES = (
        (MALE, 'мужской'),
        (FEMALE, 'женский'),
    )

    user = models.OneToOneField(ShopUser, primary_key=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='теги', max_length=128, blank=True)
    about_me = models.TextField(verbose_name='о себе', blank=True)
    gender = models.CharField(verbose_name='пол', max_length=1, choices=GENDER_CHOISES, blank=True)

