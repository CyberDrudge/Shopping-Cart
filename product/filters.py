import django_filters

from product.models import Product


class ProductFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(method='status_filter')

    class Meta:
        model = Product
        fields = ['name', 'description', 'status']

    def status_filter(self, queryset, name, value):
        status_list = value.split(",")
        return queryset.filter(status__in=status_list)
