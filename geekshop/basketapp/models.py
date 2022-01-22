from django.contrib.auth import get_user_model
from django.db import models
from mainapp.models import Product


class BasketItem(models.Model):
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField('количество', default=0)
    add_dt = models.DateTimeField('время', auto_now_add=True)
    update_dt = models.DateTimeField('время', auto_now=True)

    def delete(self):
        self.product.quantity += self.qty
        self.product.save()
        super(self.__class__, self).delete()

    def save(self, *args, **kwargs):
        if self.pk:
            self.product.quantity -= 1
            self.product.save()
        super(self.__class__, self).save(*args, **kwargs)

    @property
    def product_cost(self):
        return self.product.price * self.qty
