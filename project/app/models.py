from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class CustomUser(AbstractUser):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    account_type = models.CharField(max_length=30)
    subject = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return(f"{self.username} {self.account_type}")

class Reservation(models.Model):
    date = models.CharField(max_length=30)
    student_username = models.CharField(max_length=30, null=True, default='')
    tutor_username = models.CharField(max_length=30, null=True, default='')

    def __str__(self):
        return (f"Uczeń: {self.student_username}, Korepetytor: {self.tutor_username}, Data: {self.date}")
    
# source of user payment: https://github.com/dotja/django-example/blob/main/user_payment/models.py    
class UserPayment(models.Model):
    app_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)

@receiver(post_save, sender=CustomUser)
def create_user_payment(sender, instance, created, **kwargs):
    if created:
        UserPayment.objects.create(app_user=instance)