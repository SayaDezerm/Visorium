from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Favorite
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.

def home(request):
    genre_filter = request.GET.get('genre', '')
    movies = Movie.objects.all()

    if genre_filter:
        movies = movies.filter(genre=genre_filter)

    genres = Movie.GENRE_CHOICES

    return render(request, 'catalog/main.html', {
        'movies': movies,
        'genres': genres,
        'active_genres': genre_filter,
    })

def new_movies(request):
    now = datetime.now().year 
    new = now - 10

    movies = Movie.objects.filter(release_year__gte=new).order_by('-release_year')
    return render(request, 'catalog/new_release.html', {'movies': movies},)

@login_required
def toggle_favorites(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, movie=movie)

    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True

    return JsonResponse({'is_favorite': is_favorite, 'movie_id': movie_id})

@login_required
def watchlist(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('movie').order_by('-added_at')
    return render(request, 'catalog/watchlist.html', {'favorites': favorites})