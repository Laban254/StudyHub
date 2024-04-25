from django import template

register = template.Library()

@register.filter
def truncate_words(value, arg):
    words = value.split()[:int(arg)]
    return ' '.join(words)

@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})