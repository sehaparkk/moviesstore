from django import template
register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='get_quantity')
def get_quantity(cart, movie_id):
    if cart:
        return cart.get(str(movie_id))
    return None