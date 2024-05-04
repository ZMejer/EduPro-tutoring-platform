from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("rejestracja", views.signUpPage, name="signUpPage"),
    path("logowanie", views.loginPage, name="loginPage"),
    path('wyloguj', views.logoutUser, name='logout'),
    path("profil", views.myProfilePage, name="myProfilePage"),
    path("terminy", views.slots, name="slots"),
    path("korepetytorzy", views.tutors, name="tutors"),
    path("payment_successfull", views.payment_successfull, name="payment_successfull"),
    path("payment_cancelled", views.payment_cancelled, name="payment_cancelled"),
    path("stripe_webhook", views.stripe_webhook, name="stripe_webhook"),
]