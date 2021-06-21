
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import CustomUserManager
from accounts import validators
JOB_TYPE = (
    ('M', "Male"),
    ('F', "Female"),

)

ROLE = (
    ('employer', "Employer"),
    ('employee', "Employee"),
)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    role = models.CharField(choices=ROLE,  max_length=10)
    gender = models.CharField(choices=JOB_TYPE, max_length=1)
    phone_number = models.CharField(max_length=25, default="", validators=[validators.validate_phone_number])
    cv = models.FileField(upload_to="cv/", default='media/default.pdf', validators=[validators.validate_file_extension])


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name
    objects = CustomUserManager()


class OTPModel(models.Model):
    otp_code = models.CharField(max_length=8, unique=True)
    # Email is used to link a OTP with a user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # if Expiry is greater than the current time it is rejected
    expiry = models.DateTimeField()

    # UUID is used to redirect user to change password page
    UUID = models.CharField(max_length=50, unique=True)
