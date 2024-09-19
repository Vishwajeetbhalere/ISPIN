# main/templatetags/custom_filters.py

from django import template

register = template.Library()


@register.filter(name='add_css_class')
def add_css_class(field, css_class):
    """Adds a CSS class to a form field widget."""
    return field.as_widget(attrs={"class": css_class})
