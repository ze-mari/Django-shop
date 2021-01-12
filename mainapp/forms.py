from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order, Product


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Дата получение заказа'

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'phone', 'address', 'buying_type', 'order_date', 'comment')


class CustomerCreationForm(UserCreationForm):

    phone = forms.CharField(label="Телефон", max_length=19, required=False)
    address = forms.CharField(label="Адрес", max_length=250, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ("username", "email")


class AddSpecificationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        object_id = kwargs.get('object_id')
        del kwargs["object_id"]
        super().__init__(*args, **kwargs)
        product = Product.objects.get(id=object_id)
        specifications = product.category.related_specifications.all()
        for specification in specifications:
            self.fields[specification.slug] = forms.CharField(max_length=255,
                                                              required=specification.required,
                                                              label=specification.name)





