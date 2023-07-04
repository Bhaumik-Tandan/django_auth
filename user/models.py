from django.db import models

import random
import string

def generate_access_code():
    length = 6  # Length of the access code
    characters = string.ascii_uppercase + string.digits  # Use uppercase letters and digits for the code
    access_code = ''.join(random.choices(characters, k=length))
    return access_code

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10)
    referral_code = models.CharField(max_length=6, unique=True, null=True, blank=True)
    payment = models.DecimalField(max_digits=8, decimal_places=2)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username

