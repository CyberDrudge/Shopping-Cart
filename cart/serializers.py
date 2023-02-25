from rest_framework.serializers import ModelSerializer, CharField

from cart.models import Cart, CartItem


class CartItemSerializer(ModelSerializer):
    product = CharField()

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']


class CartSerializer(ModelSerializer):
    items = CartItemSerializer(source='get_cart_items', many=True)
    user = CharField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'amount', 'user']
