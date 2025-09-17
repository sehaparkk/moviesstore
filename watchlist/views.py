from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Watchlist
from movies.models import Movie

@login_required
def index(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    template_data = {
        'title': 'My Watchlist',
        'watchlist': watchlist
    }
    return render(request, 'watchlist/index.html', {'template_data': template_data})

@login_required
def add_to_watchlist(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    # Default rating to 1, the user can change it later
    watchlist_item, created = Watchlist.objects.get_or_create(user=request.user, movie=movie, defaults={'rating': 1})
    return redirect('watchlist.index')

@login_required
def update_rating(request, item_id):
    if request.method == 'POST':
        watchlist_item = Watchlist.objects.get(id=item_id, user=request.user)
        watchlist_item.rating = request.POST['rating']
        watchlist_item.save()
    return redirect('watchlist.index')