from django.db import models
from django.db.models.signals import post_save

from product.constants import ProductStatusChoices


class Product(models.Model):
	name = models.CharField(max_length=64)
	description = models.TextField()
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.IntegerField(default=1)
	status = models.CharField(max_length=32, choices=ProductStatusChoices.CHOICES, default=ProductStatusChoices.INACTIVE)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


def product_post_save_handler(sender, instance, created, *args, **kwargs):
	if instance.quantity == 0 and instance.status == ProductStatusChoices.AVAILABLE:
		instance.status = ProductStatusChoices.SOLD_OUT
		instance.save()
	elif instance.quantity > 0 and instance.status == ProductStatusChoices.SOLD_OUT:
		instance.status = ProductStatusChoices.AVAILABLE
		instance.save()


post_save.connect(product_post_save_handler, Product)
