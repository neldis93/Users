from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES=(

        ('M','Male'),
        ('F','Female'),
        ('0','Others'),
    )

    username = models.CharField('Username', max_length=10, unique= True)
    email = models.EmailField(unique= True) # tiene que estra en unique= True porque los correos no pueden ser iguales
    name = models.CharField('Name', max_length=30)
    last_name = models.CharField('Last name', max_length=30)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    code_register = models.CharField(max_length=6, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    USERNAME_FIELD='username'

    REQUIRED_FIELDS=['email']

    objects= UserManager()

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.name + ' ' + self.last_name

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    #def __str__(self):
     #   return return self.name + ' ' + self.last_name
        

