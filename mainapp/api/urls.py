from django.urls import path, re_path

from . import api_views


urlpatterns = [
    re_path(r'^categories/((?P<id>[0-9]+)/){0,1}$', api_views.CategoryAPIView.as_view(), name='categories'),
    path('customers/', api_views.CustomerListAPIView.as_view(), name='customers')
]



