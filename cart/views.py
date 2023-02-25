from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from cart.models import Cart
from cart.serializers import CartSerializer
from cart.service import CartService
from product.service import ProductService


class CartAPIView(CreateAPIView):
	serializer_class = CartSerializer
	queryset = Cart.objects.all()

	def get_cart_object(self):
		return CartService.get_cart_by_user(self.request.user)

	def get(self, *args, **kwargs):
		cart = self.get_cart_object()
		serializer = self.serializer_class(cart)
		return Response(serializer.data)

	def post(self, request, *args, **kwargs):
		product_id = request.data.get('product_id')
		quantity = request.data.get('quantity')

		product = ProductService.get_product_by_id(product_id)
		if not product:
			return Response({"error": "Product Not Available"}, status=400)
		if quantity < 0:
			return Response({"error": "Invalid Quantity: Quantity can not be less than 0"}, status=400)
		if quantity > product.quantity:
			return Response({"error": f"Invalid Quantity: Only {product.quantity} item(s) are available"}, status=400)

		cart = self.get_cart_object()
		CartService.update_item(cart, product, quantity)
		cart.refresh_from_db()
		serializer = self.serializer_class(cart)
		return Response(serializer.data)

	def delete(self, request, *args, **kwargs):
		cart = self.get_cart_object()
		CartService.clear_cart(cart)
		return Response({"message": "Cart removed"}, status=200)
