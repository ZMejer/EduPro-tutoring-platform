from django.contrib import admin
from .models import CustomUser, Reservation

admin.site.register(CustomUser)
admin.site.register(Reservation)
