from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='watchlist.index'),
    path('add/<int:movie_id>/', views.add_to_watchlist, name='watchlist.add'),
    path('update_rating/<int:item_id>/', views.update_rating, name='watchlist.update_rating'),
]