from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("rejestracja", views.signUpPage, name="signUpPage"),
    path("logowanie", views.loginPage, name="loginPage"),
]