from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView, View
from .models import Category, Customer, CartProduct, User, Product
from .mixins import CategoryDetailMixin, CartMixin
from .forms import OrderForm, CustomerCreationForm
from .utils import recalc_cart


class BaseView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.get_categories_for_left_sidebar()
        products = Product.objects.all().order_by('-id')[:6]
        context = {
            'categories': categories,
            'products': products,
            'cart': self.cart,
            'user': request.user,
        }
        return render(request, 'mainapp/base.html', context)


class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):

    model = Product
    template_name = 'mainapp/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):

    model = Category
    context_object_name = 'category'
    template_name = 'mainapp/category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            product_slug = kwargs.get('slug')
            product = Product.objects.get(slug=product_slug)
            cp, created = CartProduct.objects.get_or_create(
                user=self.cart.owner, cart=self.cart, product=product
            )
            if created:
                self.cart.products.add(cp)
            recalc_cart(self.cart)
            messages.add_message(request, messages.INFO, "Товар успешно добавлен!")
            return HttpResponseRedirect('/cart/')
        messages.add_message(request, messages.INFO, 'Войдите что-бы добавить товар в корзину')
        return HttpResponseRedirect('/login/')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            product_slug = kwargs.get('slug')
            product = Product.objects.get(slug=product_slug)
            cp = CartProduct.objects.get(
                user=self.cart.owner, cart=self.cart, product=product
            )
            self.cart.products.remove(cp)
            cp.delete()
            recalc_cart(self.cart)
            messages.add_message(request, messages.INFO, "Товар успешно удален!")
            return HttpResponseRedirect('/cart/')
        messages.add_message(request, messages.INFO, 'Войдите что-бы удалить товар')
        return HttpResponseRedirect('/login/')


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.get_categories_for_left_sidebar()
        context = {
            'cart': self.cart,
            'categories': categories,
        }
        return render(request, 'mainapp/cart.html', context)


class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.get_categories_for_left_sidebar()
        form = OrderForm(request.POST or None)

        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form,
        }
        return render(request, 'mainapp/checkout.html', context)


class ChangeQTYView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cp = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        qty = int(request.POST.get('qty'))
        cp.qty = qty
        cp.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Кол-во успешно изменено!")
        return HttpResponseRedirect('/cart/')


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Ваш заказ успешно оформлен, спосибо за заказ!')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


class RegistrationView(View):

    def get(self, request, *args, **kwargs):
        context = {
            "form": CustomerCreationForm,
        }
        return render(request, 'mainapp/auth.html', context)


class AuthenticationView(View):

    def post(self, request, *args, **kwargs):
        form = CustomerCreationForm(request.POST or None)
        if form.is_valid():
            form.save(commit=False)
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            customer = Customer.objects.create(
                user=user,
                phone=form.cleaned_data["phone"],
                address=form.cleaned_data["address"]
            )
            customer.save()
            messages.add_message(request, messages.INFO, "Вы зарегистрированы!")
            return HttpResponseRedirect('/')
        messages.add_message(request, messages.WARNING, "При заполнении следите за примечанием, или измените имя пользователя! ")
        return HttpResponseRedirect('/register/')


class UserPageView(LoginRequiredMixin, CartMixin, View):

    login_url = 'login'

    def get(self, request, *args, **kwargs):
        categories = Category.get_categories_for_left_sidebar()
        customer = Customer.objects.get(user=request.user)
        context = {
            'categories': categories,
            'customer': customer,
            'cart': self.cart,
        }
        return render(request, 'mainapp/user_page.html', context=context)



