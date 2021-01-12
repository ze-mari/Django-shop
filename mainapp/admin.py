from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):

    change_form_template = 'mainapp/admin.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Specification)
