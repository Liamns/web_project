from django import template

register = template.Library()

@register.filter('addresskey')
def addresskey(dict_data, key):
    if key in dict_data:
        return dict_data.get(key)
