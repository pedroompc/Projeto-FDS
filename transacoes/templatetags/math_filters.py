# filepath: transacoes/templatetags/math_filters.py
from django import template

register = template.Library()

@register.filter
def sub(value, arg):
    """Subtrai arg de value."""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0