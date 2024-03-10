from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser 

def home(request):
    return render(request, "home.html")

def signUpPage(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        user_login = request.POST.get('login')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        accountType = request.POST.get('accountType')
        if password != confirmPassword:
            messages.error(request, 'Hasła nie są identyczne. Proszę wprowadzić zgodne hasła.')
        else:
            try:
                newUser = CustomUser.objects.create_user(username=user_login, email=email, password=password, name=name, surname=surname, account_type=accountType)
                newUser.save()
                messages.success(request, 'Rejestracja zakończona pomyślnie. Możesz się teraz zalogować.')
            except Exception as e:
                messages.error(request, f'Błąd rejestracji: {e}')
    return render(request, "signup.html")

def loginPage(request):
    if request.method == 'POST':
        user_login = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(request, username=user_login, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, f'Witaj {user_login}. Jesteś teraz zalogowany.')
        else:
            messages.error(request, 'Hasło jest nieprawidłowe lub użytkownik nie istnieje.')
    return render(request, "login.html")

def logoutUser(request):
    logout(request)
    messages.success(request, 'Pomyślnie wylogowano.')
    return redirect('home')