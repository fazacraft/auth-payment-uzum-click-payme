import random
import uuid
from email.policy import default
from secrets import choice

from django.db import models

from abstract_model.base_model import BaseModel


# Create your models here.

ROLE_CHOICE = (
    (1,'customer'),
    (2,'admin'),
    (3,'superadmin'),
)



class User(BaseModel):
    full_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.PositiveSmallIntegerField(choices = ROLE_CHOICE, default = 1)
    password = models.CharField(max_length=300)
    status = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    login_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.full_name



class OTP(BaseModel):
    user = models.ForeignKey('USER', on_delete=models.CASCADE, related_name='otp_user')
    otp_key = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)
    otp_code = models.PositiveIntegerField(default=random.randint(1000,9999))
    reset = models.BooleanField(default=False)
    attempt = models.IntegerField(default=0)
