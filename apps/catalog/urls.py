from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new/', views.new_movies, name='new_release'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('favorites/<int:movie_id>/', views.toggle_favorites, name='toggle_favorite'),
]