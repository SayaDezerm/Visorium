from django.shortcuts import render
from .models import Movie
from datetime import datetime

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