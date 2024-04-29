from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from datetime import datetime, date
from dateutil.parser import parse
import json
import urllib.parse

from .models import User, Event


def index(request):
    if request.user.is_authenticated:
        curr_year = date.today().year
        curr_month = date.today().month

        return HttpResponseRedirect(reverse("month_view", args=[curr_year, curr_month]))

    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirmpassword"]

        if password != confirm_password:
            return render(
                request,
                "./calendarapp/register.html",
                {"message": "Passwords do not match"},
            )

        try:
            user = User.objects.create_user(
                email,
                password,
                first_name=request.POST["firstname"],
                last_name=request.POST["lastname"],
            )
        except IntegrityError:
            return render(
                request, "./calendarapp/register.html", {"message": "Error saving user"}
            )

        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    return render(request, "./calendarapp/register.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "./calendarapp/login.html",
                {"message": "Invalid email/password combination"},
            )

    return render(request, "./calendarapp/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


@login_required
def insert_event(request):
    if request.method == "POST":
        data = json.loads(request.body)
        description = data.get("description")
        place = data.get("place")
        datet = datetime.strptime(data.get("datet"), "%Y-%m-%d %H:%M")
        title = data.get("title")
        user = request.user

        try:
            event = Event.objects.create(
                user=user,
                description=description,
                place=place,
                datet=datet,
                title=title,
            )
        except IntegrityError:
            return render(
                request, "./calendarapp/event.html", {"message": "Error saving event"}
            )

        return redirect("index")
    else:
        return render(request, "./calendarapp/event.html")


@login_required
def event_list(request):
    events = Event.objects.filter(user=request.user).order_by("-date")
    return render(request, "./calendarapp/event_list.html", {"events": events})


@login_required
def day_list(request, date):
    date = urllib.parse.unquote(date)
    date = parse(date).date()
    events = Event.objects.filter(user=request.user, date=date)
    return render(
        request, "./calendarapp/day_list.html", {"events": events, "date": date}
    )


@login_required
def event_delete(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return HttpResponseRedirect(reverse("event_list"))


@login_required()
def month_view(request, year, month):
    event_list = [
        str(date)
        for date in list(
            Event.objects.filter(user=request.user).values_list("date", flat=True)
        )
    ]

    prev_year = year if month > 1 else year - 1
    next_year = year if month < 12 else year + 1
    prev_month = month - 1 if month > 1 else 12
    next_month = month + 1 if month < 12 else 1

    return render(
        request,
        "./calendarapp/month_view.html",
        {
            "event_list": event_list,
            "prev_year": prev_year,
            "next_year": next_year,
            "prev_month": prev_month,
            "next_month": next_month,
            "year": year,
            "month": month,
        },
    )
