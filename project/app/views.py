from django.shortcuts import render, HttpResponse

def home(request):
    return render(request, "home.html")

def signUpPage(request):
    return render(request, "signup.html")

def loginPage(request):
    return render(request, "login.html")