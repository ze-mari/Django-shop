from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name="Имя категории")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    @staticmethod
    def get_categories_for_left_sidebar():
        categories = Category.objects.all().order_by('id')
        categories_with_product_counts = [{'name': ct.name, 'count': ct.products.count(), 'slug': ct.slug} for ct in categories]
        return categories_with_product_counts


class Product(models.Model):

    category = models.ForeignKey(to=Category, verbose_name="Катерогия", on_delete=models.CASCADE,
                                 related_name='products')
    title = models.CharField(max_length=255, verbose_name="Наименование")
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name="Изоброжение")
    description = models.TextField(verbose_name="Описание", null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Цена")
    specifications = models.JSONField(null=True, editable=False)

    def __str__(self):
        return self.title


class Specification(models.Model):

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE,
                                 related_name='related_specifications')
    name = models.CharField(max_length=150, verbose_name='Название спецификации')
    slug = models.SlugField(unique=True)
    required = models.BooleanField(verbose_name='Обязательно для заполнение')


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name="Покупатель", on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name="Карзина", on_delete=models.CASCADE, related_name='related_products')
    product = models.ForeignKey('Product', verbose_name='Продукт', on_delete=models.CASCADE)
    qty = models.IntegerField(default=1, verbose_name="Количество")
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Общая цена")

    def __str__(self):
        return "Продукт: {}".format(self.product.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', null=True, verbose_name="Владелец", on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name="Общая цена карзины")
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Номер телефона")
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Адрес")
    orders = models.ManyToManyField('Order', verbose_name="заказы покупателя",
                                    related_name='related_customer', blank=True)

    def __str__(self):
        return "Покупатель: {}".format(self.user.username)


class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = {
        (STATUS_NEW, "Новый заказ"),
        (STATUS_IN_PROGRESS, "Заказ в обработке"),
        (STATUS_READY, "Заказ готов"),
        (STATUS_COMPLETED, "Заказ выполнен"),
    }

    BUYING_TYPE_CHOICES = {
        (BUYING_TYPE_SELF, "Самовывоз"),
        (BUYING_TYPE_DELIVERY, "Доставка"),
    }

    customer = models.ForeignKey(Customer, verbose_name="Покупатель",
                                 related_name='related_orders', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name="корзина", on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=1024, verbose_name="Адрес", null=True, blank=True)
    status = models.CharField(max_length=100, verbose_name="Статус", choices=STATUS_CHOICES, default=STATUS_NEW)
    buying_type = models.CharField(
        max_length=100,
        verbose_name="Тип заказа",
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name="Коментарий к заказу", null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name="Дата создание заказа")
    order_date = models.DateField(verbose_name="Дата получение заказа", default=timezone.now)

    def __str__(self):
        return str(self.id)

    def get_status_verbose_name(self):
        for item in self.STATUS_CHOICES:
            if item[0] == self.status:
                return item[1]
        return None
