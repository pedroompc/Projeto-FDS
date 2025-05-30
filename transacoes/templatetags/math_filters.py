from django import template

register = template.Library()

@register.filter
def sub(value, arg):
    """Subtract the arg from the value."""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return value
        
@register.filter
def div(value, arg):
    """Divide the value by the arg."""
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return value

@register.filter
def mul(value, arg):
    """Multiply the value with the arg."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return value

@register.filter
def get_item(list_or_dict, key_or_index):
    """
    Get an item from a list by index or from a dictionary by key.
    Used like: {{ mylist|get_item:index }}
    """
    try:
        return list_or_dict[key_or_index]
    except (IndexError, KeyError, TypeError):
        return None