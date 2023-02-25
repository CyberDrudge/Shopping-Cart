from product.constants import ProductStatusChoices
from product.models import Product


class ProductService:
	@classmethod
	def get_product_by_id(cls, product_id):
		try:
			return Product.objects.filter(id=product_id, quantity__gt=0, status=ProductStatusChoices.AVAILABLE).last()
		except Product.DoesNotExist:
			return None
