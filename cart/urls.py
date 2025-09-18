from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='cart.index'),
    path('<int:id>/add/', views.add, name='cart.add'),
    path('<str:cart_id>/clear/', views.clear, name='cart.clear'),
    path('<str:cart_id>/purchase/', views.purchase, name='cart.purchase'),
]