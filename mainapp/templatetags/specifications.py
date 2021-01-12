from django import template
from django.utils.safestring import mark_safe
from ..models import Specification

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


def get_product_spec(product):
    spec = product.specifications
    table_content = ''
    for key, value in spec.items():
        name = Specification.objects.get(slug=key).name
        table_content += TABLE_CONTENT.format(name=name, value=value)
    return table_content


@register.filter
def product_spec(product):
    return mark_safe(TABLE_HEAD + get_product_spec(product) + TABLE_TAIL)


