from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from datetime import datetime
import json

from .models import User, Event


# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return render(request, './calendarapp/index.html', {"user": request.user})
    return HttpResponseRedirect(reverse('login'))


def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']

        if password != confirm_password:
            return render(request, './calendarapp/register.html', {"message": "Passwords do not match"})

        try:
            user = User.objects.create_user(email, password, first_name=request.POST['firstname'],
                                            last_name=request.POST['lastname'])
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


@login_required
def insert_event(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        description = data.get('description')
        place = data.get('place')
        date = datetime.strptime(data.get('datetime'), '%Y-%m-%d %H:%M')
        title = data.get('title')
        user = request.user


        try:
            event = Event.objects.create(user=user, description=description, place=place, date=date, title=title)
        except IntegrityError:
            return render(request, './calendarapp/event.html', {"message": "Error saving event"})

        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, './calendarapp/event.html')


@login_required
def event_list(request):
    events = Event.objects.all().order_by('-date')
    return render(request, './calendarapp/event_list.html', {"events": events})


@login_required
def event_delete(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return HttpResponseRedirect(reverse('event_list'))