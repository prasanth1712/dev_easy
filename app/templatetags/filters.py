from django import template

register = template.Library()

@register.filter
def lsplit(value,pos):
    lst = str(value).rsplit('/',1)
    return lst[pos]