from django import template
from django.utils.safestring import mark_safe

register = template.Library()


TABLE_HEAD = """
             <table class="table">
                 <tbody>
             """
TABLE_TAIL = """
                 </tbody>
             </table>
             """


TABLE_CONTENT = """
                    <tr>
                      <td>{name}</td>
                      <td>{value}</td>
                    </tr>
                """


PRODUCT_SPEC = {
    "notebook": {
        'Диагональ': 'diagonal',
        'Тип дисплейа': 'display_type',
        'Частота процессора': 'processor_freq',
        'Оперативная память': 'ram',
        'Видекарта': 'video',
        'Время работы аккумулятора': 'time_without_charge',
    },
    'smartphone': {
        'Диагональ': 'diagonal',
        'Тип дисплейа': 'display_type',
        'Оперативная память': 'ram',
        'Разрешение экрана': 'resolution',
        'Объем батареи': 'accum_volume',
        'Разъём для карта памяти': 'sd',
        'Максимальный объем сд карты': 'sd_volume',
        'Главная камера': 'main_cam_mp',
        'Фронтальная камера': 'front_cam_mp',
    }
}


def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    if model_name == 'smartphone':
        if not product.sd:
            PRODUCT_SPEC['smartphone'].pop('Максимальный объем сд карты')
        else:
            PRODUCT_SPEC['smartphone']['Максимальный объем сд карты'] = 'sd_volume'
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)


