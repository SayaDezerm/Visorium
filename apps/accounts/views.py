from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib import messages
from apps.catalog.models import Favorite
from django.contrib.auth.decorators import login_required

# Create your views here.

# logica pentru log-in
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, "Utilizator sau parola incorecta.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})
    
def logout_view(request):
    logout(request)
    return redirect('home')

# logica pentru crearea contului
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bun venit {user.username}')
            return redirect('home')
        else:
            messages.error(request, 'Corecteaza erorile.')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {"form": form})

# datele pentru pagina Profile
@login_required
def profile_view(request):

    recent_favorites = (Favorite.objects.filter(user=request.user).select_related('movie').order_by('-added_at')[:6])

    from django.db.models import Count
    top_genre = (Favorite.objects.filter(user=request.user).values('movie__genre').annotate(count=Count('id')).order_by('-count').first())

    favorite_genre = top_genre['movie__genre'].capitalize() if top_genre else None

    return render(request, 'accounts/profile.html', {
        'recent_favorites': recent_favorites,
        'favorite_genre': favorite_genre,
        'total_favorites': Favorite.objects.filter(user=request.user).count(),
    })

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Parola modificata cu succes.')
            return redirect('profile')
        else:
            messages.error(request, 'Corecteaza erorile de mai jos.')
    
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})