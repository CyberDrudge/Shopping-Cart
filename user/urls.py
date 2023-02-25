from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    url(r'^send-otp/$', views.SendOTPRequestAPIView.as_view()),
    url(r'^register/$', views.RegisterAPIView.as_view()),
    url(r'^login/$', views.LoginAPIView.as_view()),
    url(r'^logout/$', views.LogoutAPIView.as_view()),
    url(r'^(?P<pk>[0-9]+)/update/$', views.UserUpdateAPIView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
