from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    account_type = models.CharField(max_length=30)
    subject = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return(f"{self.username} {self.account_type}")
