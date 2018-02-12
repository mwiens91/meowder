"""Contains custom template filters."""

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary."""
    return dictionary.get(key)

@register.simple_tag
def call_method(obj, method_name, *args):
    """Call a function with arguments."""
    method = getattr(obj, method_name)
    return method(*args)
