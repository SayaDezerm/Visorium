from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages

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