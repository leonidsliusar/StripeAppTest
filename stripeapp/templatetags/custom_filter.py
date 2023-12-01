from django import template

register = template.Library()


@register.filter(name="c2doll")
def divide_by_100(value):
    return value / 100
