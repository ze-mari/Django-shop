from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from .serializers import CategorySerializer, CustomerSerializer
from ..models import Category, Customer


class CategoryPagination(PageNumberPagination):

    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10


class CategoryAPIView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):

    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
    queryset = Category.objects.all().order_by('id')
    lookup_field = 'id'


class CustomerListAPIView(ListAPIView):

    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()



