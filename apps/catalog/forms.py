from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'image', 'genre', 'duration', 'release_year']
        widgets = {
            'title':        forms.TextInput(attrs={'placeholder': 'Titlul filmului'}),
            'description':  forms.Textarea(attrs={'placeholder': 'Descriere...', 'rows': 4}),
            'genre':        forms.Select(),
            'duration':     forms.NumberInput(attrs={'placeholder': 'minute'}),
            'release_year': forms.NumberInput(attrs={'placeholder': '2024'}),
        }