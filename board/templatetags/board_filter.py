from django import template

register = template.Library()

@register.filter
def sub(value, arg):    #기존값(value)에서 arg를 빼서 반환함
    return value - arg

