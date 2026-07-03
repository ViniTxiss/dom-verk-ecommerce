from django import template

register = template.Library()

@register.filter(name='first_name')
def first_name(value):
    """Retorna o primeiro nome de uma string de nome completo."""
    if not value:
        return ''
    return str(value).split()[0]
