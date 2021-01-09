from rest_framework import serializers
from ..models import Category, Customer, Order


class CategorySerializer(serializers.ModelSerializer):

    name = serializers.CharField()
    slug = serializers.SlugField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug',
        ]


class BaseProductSerializer:

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects)
    title = serializers.CharField()
    slug = serializers.SlugField()
    image = serializers.ImageField()
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=9, decimal_places=2)


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):

    orders = OrderSerializer(many=True)

    class Meta:
        model = Customer
        fields = '__all__'



