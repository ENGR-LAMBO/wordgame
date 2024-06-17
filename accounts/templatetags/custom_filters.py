# accounts/templatetags/custom_filters.py:
# accounts/templatetags/custom_filters.py:
from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    try:
        return value.as_widget(attrs={'class': arg})
    except AttributeError:
        return value  # or raise an appropriate error/message

