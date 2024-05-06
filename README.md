# [EduPro](http://eduprotutoring.pythonanywhere.com "EduPro") :uk:

EduPro is a website built with Django, designed for tutors and students to schedule tutoring sessions. 

## Features
- **Schedule Tutoring Sessions**: Tutors and students can easily schedule tutoring sessions according to their availability.
- **User-friendly Interface**: Intuitive design for seamless navigation and usability.

## Installation
To run EduPro locally, follow these steps:

1. Clone this repository.
2. Install the dependencies using `pip install -r requirements.txt`.
3. Run the server using `python manage.py runserver`.
4. To use stripe payment system locally, install Stripe CLI (instructions here: https://docs.stripe.com/stripe-cli)
5. Run stripe locally using `stripe listen --forward-to http://127.0.0.1:8000/stripe_webhook --api-key [insert api key here]`.


## Usage
1. Visit [EduPro](http://eduprotutoring.pythonanywhere.com).
2. Sign up for an account as a tutor or a student.
3. Start scheduling your tutoring sessions!
4. To use the test payment system, your card number should be: `4242 4242 4242 4242`

<br></br>
# [EduPro](http://eduprotutoring.pythonanywhere.com "EduPro") :poland:

EduPro to strona internetowa stworzona przy użyciu Django, zaprojektowana dla korepetytorów i uczniów, aby umawiać się na korepetycje.

## Funkcje
- **Umawianie się na Korepetycje**: Korepetytorzy i uczniowie mogą łatwo umawiać się na korepetycje zgodnie z własną dostępnością.
- **Przyjazny Interfejs Użytkownika**: Intuicyjny design dla płynnej nawigacji i łatwości użytkowania.

## Instalacja
Aby uruchomić EduPro lokalnie, wykonaj następujące kroki:

1. Sklonuj to repozytorium.
2. Zainstaluj wymagane zależności za pomocą `pip install -r requirements.txt`.
3. Uruchom serwer za pomocą `python manage.py runserver`.
4. Aby używać lokalnie systemu płatności Stripe, zainstaluj Stripe CLI (instrukcje znajdziesz tutaj: https://docs.stripe.com/stripe-cli)
5. Uruchom Stripe lokalnie za pomocą `stripe listen --forward-to http://127.0.0.1:8000/stripe_webhook --api-key [wstaw tutaj swój klucz API]`.

## Użycie
1. Odwiedź [EduPro](http://eduprotutoring.pythonanywhere.com).
2. Zarejestruj się jako korepetytor lub uczeń.
3. Zacznij umawiać się na korepetycje!
4. Aby użyć testowego systemu płatności, numer twojej karty powinien być: `4242 4242 4242 4242`

