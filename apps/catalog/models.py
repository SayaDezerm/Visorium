from django.db import models

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
    image = models.ImageField(upload_to='posters/')
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    duration = models.IntegerField(blank=True, null=True)
    release_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} - {self.release_year}" 
