from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from movies.models import Movie
from .utils import calculate_cart_total
from .models import Order, Item
from django.contrib.auth.decorators import login_required

def index(request):
    cart_id = request.GET.get('cart_id', "1")
    cart_total = 0
    movies_in_cart = []
    cart = request.session.get('cart', {}).get(cart_id, {})
    movie_ids = list(cart.keys())
    if (movie_ids != []):
        movies_in_cart = Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart, movies_in_cart)

    template_data = {}
    template_data['title'] = f'Cart {cart_id}'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    template_data['cart_id'] = cart_id
    template_data['carts'] = ["1", "2", "3"]
    return render(request, 'cart/index.html', {'template_data': template_data})

def add(request, id):
    get_object_or_404(Movie, id=id)
    cart_id = request.POST.get('cart_id', "1")
    cart = request.session.get('cart', {})
    if cart_id not in cart:
        cart[cart_id] = {}
    cart[cart_id][id] = request.POST['quantity']
    request.session['cart'] = cart
    return redirect(f'/cart/?cart_id={cart_id}')

def clear(request, cart_id):
    cart = request.session.get('cart', {})
    if cart_id in cart:
        cart[cart_id] = {}
    request.session['cart'] = cart
    return redirect(f'/cart/?cart_id={cart_id}')

@login_required
def purchase(request, cart_id):
    cart = request.session.get('cart', {}).get(cart_id, {})
    movie_ids = list(cart.keys())
    if (movie_ids == []):
        return redirect(f'/cart/?cart_id={cart_id}')
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)
    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()
    for movie in movies_in_cart:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = cart[str(movie.id)]
        item.save()
    
    # Clear the purchased cart
    session_cart = request.session.get('cart', {})
    if cart_id in session_cart:
        session_cart[cart_id] = {}
    request.session['cart'] = session_cart

    template_data = {}
    template_data['title'] = 'Purchase confirmation'
    template_data['order_id'] = order.id
    return render(request, 'cart/purchase.html',
        {'template_data': template_data})