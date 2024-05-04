from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, Reservation, UserPayment
import calendar
from datetime import datetime, timedelta
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
import stripe
import time
from django.views.decorators.csrf import csrf_exempt

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
        subject = request.POST.get('subject')
        if password != confirmPassword:
            messages.error(request, 'Hasła nie są identyczne. Proszę wprowadzić zgodne hasła.')
        else:
            try:
                newUser = CustomUser.objects.create_user(username=user_login, email=email, password=password, name=name, surname=surname, account_type=accountType, subject=subject)
                newUser.save()
                messages.success(request, 'Rejestracja zakończona pomyślnie. Możesz się teraz zalogować.')
                return redirect('loginPage')
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
            return redirect('home')
        else:
            messages.error(request, 'Hasło jest nieprawidłowe lub użytkownik nie istnieje.')
    return render(request, "login.html")

def logoutUser(request):
    logout(request)
    messages.success(request, 'Pomyślnie wylogowano.')
    return redirect('home')

def myProfilePage(request):
    if request.user.is_authenticated:
        reservations_data = []
        if request.user.account_type == 'student':
            reservations = Reservation.objects.filter(student_username=request.user.username)
            reservations = reservations.order_by('date')
            for i in range(len(reservations)):
                tutor_username_res = Reservation.objects.filter(Q(student_username=request.user.username) & Q(date=reservations[i].date))
                tutors_username = list(tutor_username_res.values_list('tutor_username', flat=True))[0]
                tutors_object = CustomUser.objects.filter(username=tutors_username)
                tutors_data = list(tutors_object.values_list('name','surname')[0])
                tutors_name = tutors_data[0] + " " + tutors_data[1]
                reservations_data.append(f"Data: {reservations[i].date}, Korepetytor: {tutors_name}")
        elif request.user.account_type == 'tutor':
            reservations = Reservation.objects.filter(tutor_username=request.user.username)
            reservations = reservations.order_by('date')
            for i in range(len(reservations)):
                student_username_res = Reservation.objects.filter(Q(tutor_username=request.user.username) & Q(date=reservations[i].date))
                students_username = list(student_username_res.values_list('student_username', flat=True))[0]
                students_object = CustomUser.objects.filter(username=students_username)
                students_data = list(students_object.values_list('name','surname')[0])
                students_name = students_data[0] + " " + students_data[1]
                reservations_data.append(f"Data: {reservations[i].date}, Uczeń: {students_name}")
        return render(request, 'profile.html', {'reservations': reservations_data})
    else:
        return render(request, 'profile.html')

def slots(request):
    now = timezone.localtime(timezone.now())
    cal = calendar.monthcalendar(now.year, now.month)
    month = now.month
    weekdays = calendar.weekheader(3).split()
    for week in cal:
        for day in range(len(week)):
            if week[day] == 0:
                week[day] = None
    hours = range(8,19)
    users = CustomUser.objects.all()
    prev_month=month-1
    for i in range(0,32):
        for j in range(0,19):
            if i < 10:
                Reservation.objects.filter(date="0"+str(i)+".0"+str(prev_month)+" "+str(j)+":00").delete()
            else:
                Reservation.objects.filter(date=str(i)+".0"+str(prev_month)+" "+str(j)+":00").delete()
    if request.method == 'POST':
        if request.POST.get("form_type") == 'selectTutor':
            tutor_login = request.POST.get('tutor')
            tutors_object = CustomUser.objects.filter(username=tutor_login)
            tutors_data = list(tutors_object.values_list('name','surname')[0])
            tutors_name = tutors_data[0] + " " + tutors_data[1]
            taken_slots_objects = Reservation.objects.filter(tutor_username=tutor_login)
            taken_slots = list(taken_slots_objects.values_list('date', flat=True))
            taken_dates = [int(slot.split()[0][:-3]) for slot in taken_slots]
            taken_hours = [int(slot.split()[1][:-3]) for slot in taken_slots]
            return render(request, "slots.html", {'cal': cal, 'weekdays': weekdays, 'hours': hours, 'users': users, 'month': month, 'current_day':now.day,'current_hour':now.hour,'chosen_tutor_name':tutors_name, 'chosen_tutor_username':tutor_login, 'taken_dates':taken_dates, 'taken_hours':taken_hours})
        elif request.POST.get("form_type") == 'selectDate':
            request.session['student_login'] = str(request.user.username)
            request.session['tutor_login'] = request.POST.get('chosenTutor')
            request.session['date'] = request.POST.get('selected_hours')
        # Payment system (source: https://github.com/dotja/django-example/blob/main/user_payment/views.py)
        stripe.api_key = 'sk_test_51PCpbN2LfliGhtUejICAbYZ1jWXGLgdksMGluf0faJpGMaRdGRPwqlbv7T7RVWCsm1WKqUWfiqhEnRtbT2TsY3Qe00nti2IPQo'
        checkout_session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
            line_items = [
                {
                    'price': 'price_1PCpnP2LfliGhtUedYKzjbP9',
                    'quantity': 1,
                },
            ],
            mode = 'payment',
            customer_creation = 'always',
            success_url = 'http://127.0.0.1:8000/payment_successfull?session_id={CHECKOUT_SESSION_ID}',
            cancel_url = 'http://127.0.0.1:8000/payment_cancelled',
        )
        return redirect(checkout_session.url, code=303)
    return render(request, "slots.html", {'cal': cal, 'weekdays': weekdays, 'hours': hours, 'users': users, 'month': month, 'current_day':now.day, 'current_hour':now.hour})

def payment_successfull(request):
    student_login = request.session.get('student_login')
    tutor_login = request.session.get('tutor_login')
    date = request.session.get('date')
    if student_login and tutor_login and date:
        try:
            new_reservation = Reservation.objects.create(date=date, student_username=student_login, tutor_username=tutor_login)
            new_reservation.save()
            messages.success(request, 'Rezerwacja została potwierdzona.')
        except Exception as e:
            messages.error(request, f'Błąd rezerwacji: {e}')
        del request.session['student_login']
        del request.session['tutor_login']
        del request.session['date'] 
    else:
        messages.error(request, 'Brak danych rezerwacji w sesji.')   
    return render(request, "payment_successfull.html")


def payment_cancelled(request):
    del request.session['student_login']
    del request.session['tutor_login']
    del request.session['date'] 
    return render(request, "payment_cancelled.html")

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = 'sk_test_51PCpbN2LfliGhtUejICAbYZ1jWXGLgdksMGluf0faJpGMaRdGRPwqlbv7T7RVWCsm1WKqUWfiqhEnRtbT2TsY3Qe00nti2IPQo'
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)
        user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
        line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
        user_payment.payment_bool = True
        user_payment.save()
    return HttpResponse(status=200)

def tutors(request):
    users = CustomUser.objects.all()
    return render(request, 'tutors.html', {'users': users})