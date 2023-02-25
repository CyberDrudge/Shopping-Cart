from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from user.authentications import IsAuthenticatedReadsOrAdminWrites
from product.filters import ProductFilter
from product.models import Product
from product.serializers import ProductSerializer


class ProductAPIView(ListCreateAPIView):
	permission_classes = (IsAuthenticatedReadsOrAdminWrites, )
	serializer_class = ProductSerializer
	queryset = Product.objects.all().order_by('status')
	filter_backends = (filters.DjangoFilterBackend, SearchFilter,)
	filter_class = ProductFilter
	pagination_class = PageNumberPagination

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response(serializer.data)
		return Response({"error": "Something Went Wrong"}, status=500)


class ProductUpdateAPIView(RetrieveUpdateAPIView):
	permission_classes = (IsAdminUser, )
	serializer_class = ProductSerializer
	queryset = Product.objects.all()

	def patch(self, request, *args, **kwargs):
		return super(ProductUpdateAPIView, self).patch(request, *args, **kwargs)

