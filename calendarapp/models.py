from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
=======
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
>>>>>>> d136360 (Add Tailwind CSS support)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
<<<<<<< HEAD
            raise ValueError("The Email field must be set")
=======
            raise ValueError('The Email field must be set')
>>>>>>> d136360 (Add Tailwind CSS support)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
<<<<<<< HEAD
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
=======
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
>>>>>>> d136360 (Add Tailwind CSS support)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

<<<<<<< HEAD
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return str(self.email)
=======
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
>>>>>>> d136360 (Add Tailwind CSS support)


class Event(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
<<<<<<< HEAD
    datet = models.DateTimeField()
    date = models.DateField()
    place = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.date = self.datet.date()
        super().save(*args, **kwargs)
=======
    time = models.DateTimeField()
    place = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
>>>>>>> d136360 (Add Tailwind CSS support)
