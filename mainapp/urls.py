from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.BaseView.as_view(), name='base'),
    path('products/<str:slug>', views.ProductDetailView.as_view(), name='product_detail'),
    path('categories/<str:slug>', views.CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>', views.AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart<str:slug>', views.DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-qty/<str:slug>', views.ChangeQTYView.as_view(), name='change_qty'),
    path('ckeckout/', views.CheckoutView.as_view(), name='checkout'),
    path('make-order/', views.MakeOrderView.as_view(), name='make_order'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('auth/', views.AuthenticationView.as_view(), name='auth'),
    path('login/', LoginView.as_view(template_name='mainapp/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='mainapp/base.html', next_page='base'), name='logout'),
    path('user-page/', views.UserPageView.as_view(), name='user_page'),
    path('products/add-specification/<str:object_id>', views.AddSpecificationView.as_view(), name='add_specification')
]
