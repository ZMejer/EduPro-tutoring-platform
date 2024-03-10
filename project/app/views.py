from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    return render(request, "home.html")

def signUpPage(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        login = request.POST.get('login')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        type = request.POST.get('gridRadios')
        if password != confirmPassword:
            messages.error(request, 'Hasła nie są identyczne. Proszę wprowadzić zgodne hasła.')
        else:
            try:
                newUser = User.objects.create_user(login, email, password)
                newUser.save()
                messages.success(request, 'Rejestracja zakończona pomyślnie. Możesz się teraz zalogować.')
            except Exception as e:
                messages.error(request, f'Błąd rejestracji: {e}')
    return render(request, "signup.html")

def loginPage(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
    return render(request, "login.html")