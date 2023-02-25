from django.db import models
from django.db.models.signals import post_save

from product.models import Product
from user.models import User


class Cart(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def get_cart_items(self):
		return self.cartitem_set.filter(quantity__gt=0)


class CartItem(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	created_at = models.DateTimeField(auto_now_add=True)


def cart_item_post_save_handler(sender, instance, created, *args, **kwargs):
	"""
	Handles processing after a cart is created or updated.
	"""
	from cart.service import CartService
	CartService.update_cart_amount(instance.cart)


post_save.connect(cart_item_post_save_handler, CartItem)
