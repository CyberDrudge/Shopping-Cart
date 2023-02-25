from django.contrib.auth import get_user_model
from rest_framework import serializers

user_model = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = ('id', 'contact_number', 'first_name', 'last_name', 'is_blacklisted', 'is_staff')
