from cart.models import Cart, CartItem


class CartService:
	@classmethod
	def get_cart_by_user(cls, user):
		"""
		Fetches active cart for a user. A user should have atmost 1 active cart.
		"""
		cart, created = Cart.objects.get_or_create(user=user, is_active=True)
		return cart

	@classmethod
	def update_item(cls, cart, product, quantity):
		"""
		Updated cart and its items
		"""
		cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})
		if not created:
			cart_item.quantity = quantity
			cart_item.save()

	@classmethod
	def update_cart_amount(cls, cart):
		"""
		Updates Cart's Amount
		"""
		amount = 0
		cart_items = cart.cartitem_set.all()
		for item in cart_items:
			amount += item.product.price * item.quantity
		cart.amount = amount
		cart.save()

	@classmethod
	def clear_cart(cls, cart):
		"""
		Removes all items from a cart.
		"""
		cart_items = cart.cartitem_set.all()
		for item in cart_items:
			item.quantity = 0
			item.save()
