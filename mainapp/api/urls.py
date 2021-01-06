from django.urls import path, re_path

from . import api_views


urlpatterns = [
    re_path(r'^categories/((?P<id>[0-9]+)/){0,1}$', api_views.CategoryAPIView.as_view(), name='categories'),
    path('smartphones/', api_views.SmartphoneListAPIView.as_view(), name='smartphones'),
    path('notebooks/', api_views.NotebookListAPIView.as_view(), name='notebooks'),
    path('smartphones/<str:id>/', api_views.SmartphoneDetailApiView.as_view(), name='smartphone_details'),
    path('customers/', api_views.CustomerListAPIView.as_view(), name='customers')
]



