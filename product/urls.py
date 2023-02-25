from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    url(r'^$', views.ProductAPIView.as_view(), name="create_booking"),
    url(r'^(?P<pk>[0-9]+)/update/$', views.ProductUpdateAPIView.as_view(), name="update_booking")
]

urlpatterns = format_suffix_patterns(urlpatterns)
