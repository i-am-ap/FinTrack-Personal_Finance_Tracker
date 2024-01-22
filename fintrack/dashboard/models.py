from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    


class Data(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    account = models.CharField(max_length=20, choices=[('Cash', 'Cash'), ('Card', 'Card'), ('UPI', 'UPI'), ('Account', 'Account')])
    date = models.DateField()
    time = models.TimeField(default='00:00:00')
    description = models.TextField()
    category_type = models.CharField(max_length=10, choices=[('Income', 'Income'), ('Expense', 'Expense')])

    def __str__(self):
        return self.description
    
class limitData(models.Model):
    category = models.CharField(max_length=100)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return self.category