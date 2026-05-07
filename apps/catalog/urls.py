from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new/', views.new_movies, name='new_release'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('favorites/<int:movie_id>/', views.toggle_favorites, name='toggle_favorite'),
    path('search/', views.search, name='search'),

    # admin panel custom
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/add/', views.admin_add_movie, name='admin_add_movie'),
    path('dashboard/delete/<int:movie_id>/', views.admin_delete_movie, name='admin_delete_movie'),
]