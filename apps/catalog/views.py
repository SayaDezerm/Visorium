from django.shortcuts import render
from .models import Movie

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
