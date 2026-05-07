from django.db import models
from django.contrib.auth.models import User


# model for saving movies
class Movie(models.Model):
    GENRE_CHOICES = [
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
        ('sci-fi', 'Sci-Fi'),
        ('thriller', 'Thriller'),
        ('romance', 'Romance'),
        ('documentary', 'Documentary'),
    ]

    title = models.CharField(max_length=70)
    description = models.TextField()
    image = models.ImageField(upload_to='posters/', null=True, blank=True)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    duration = models.IntegerField(blank=True, null=True)
    release_year = models.IntegerField()
    trailer_url = models.URLField(blank=True, null=True, help_text="URL YouTube (ex: https://www.youtube.com/watch?v=xxx)")

    def get_youtube_embed(self):
        if not self.trailer_url:
            return None
        if 'watch?v=' in self.trailer_url:
            video_id = self.trailer_url.split('watch?v=')[-1].split('&')[0]
        elif 'youtu.be/' in self.trailer_url:
            video_id = self.trailer_url.split('youtu.be/')[-1].split('?')[0]
        else:
            return None
        return f"https://www.youtube.com/embed/{video_id}"

    def __str__(self):
        return f"{self.title} - {self.release_year}" 

# model for saving to favorites
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="favorited_by")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"