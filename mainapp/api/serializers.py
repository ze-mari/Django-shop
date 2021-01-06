from rest_framework import serializers
from ..models import Category, Smartphone, Notebook, Customer, Order


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


class SmartphoneSerializer(BaseProductSerializer, serializers.ModelSerializer):
    
    diagonal = serializers.CharField()
    display_type = serializers.CharField()
    resolution = serializers.CharField()
    accum_volume = serializers.CharField()
    ram = serializers.CharField()
    sd = serializers.BooleanField()
    sd_volume = serializers.CharField()
    main_cam_mp = serializers.CharField()
    front_cam_mp = serializers.CharField()

    class Meta:
        model = Smartphone
        fields = '__all__'


class NotebookSerializer(BaseProductSerializer, serializers.ModelSerializer):

    diagonal = serializers.CharField()
    display_type = serializers.CharField()
    processor_freq = serializers.CharField()
    ram = serializers.CharField()
    video = serializers.CharField()
    time_without_charge = serializers.CharField()

    class Meta:
        model = Notebook
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):

    orders = OrderSerializer(many=True)

    class Meta:
        model = Customer
        fields = '__all__'



