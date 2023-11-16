from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from .models import User, Event


# Create your views here.


def index(request):
    return render(request, './calendarapp/index.html', { "user": "default"})


def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']

        if password != confirm_password:
            return render(request, './calendarapp/register.html', {"message": "Passwords do not match"})

        try:
            user = User.objects.create_user(email, password, first_name=request.POST['firstname'], last_name=request.POST['lastname'])
        except IntegrityError:
            return render(request, './calendarapp/register.html', {"message": "Error saving user"})

        login(request, user)
        return HttpResponseRedirect(reverse('index'))

    return render(request, './calendarapp/register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, './calendarapp/login.html', {'message': 'Invalid email/password combination'})

    return render(request, './calendarapp/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))