from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm
from .models import *


# class NotebookAdminForm(ModelForm):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['image'].help_text = mark_safe(
#             '<span style="color:red;">загружвйте изображение с минималным разрешением {}x{}</span>'.format(
#                 *Product.MIN_RESOLUTION
#             )
#         )
#
#     # def clean_image(self):
#     #     image = self.cleaned_data['image']
#     #     img = Image.open(image)
#     #     min_height, min_width = Product.MIN_RESOLUTION
#     #     max_height, max_width = Product.MAX_RESOLUTION
#     #     if image.size > Product.MAX_IMAGE_SIZE:
#     #         raise ValidationError('Размер изоброжения не должно превышать 3MB!')
#     #     if img.height < min_height or img.width < min_width:
#     #         raise ValidationError('Разрешение изоброжения меньше минимального!')
#     #     if img.height > max_height or img.width > max_width:
#     #         raise ValidationError('Разрешение изоброжения больше максимального!')
#     #     return image


class SmartphoneAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance is not None:
            if not instance.sd:
                self.fields.get('sd_volume').widget.attrs.update({
                    'readonly': True, 'style': 'background:lightgray;'
                })

    def clean(self):
        if not self.cleaned_data['sd']:
            self.cleaned_data['sd_volume'] = None
        return self.cleaned_data


class NotebookAdmin(admin.ModelAdmin):

    # form = NotebookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(self, db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):

    change_form_template = 'mainapp/admin.html'
    form = SmartphoneAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super(SmartphoneAdmin, self).formfield_for_foreignkey(self, db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Customer)
admin.site.register(Order)
