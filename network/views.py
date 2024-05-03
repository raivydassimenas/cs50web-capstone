import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Comment


def index(request):

    new_post = True if request.user.is_authenticated else False
    
    return render(request, "network/index.html", { "new_post": new_post })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt    
@login_required
def new_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)
    
    data = json.loads(request.body)
    author = request.user
    title = data.get("title", "")
    body = data.get("body", "")

    post = Post(
        author=author,
        title=title,
        body=body
    )
    post.save()

    return JsonResponse({"message": "Post saved successfully."}, status=201)
    

def all_posts(request):
    all_posts = Post.objects.all().order_by("created").desc()
    return JsonResponse([post.serialize() for post in all_posts], safe=False)

@login_required
def profile(request):
    followers_count = request.user.followers.all().count()
    following_count = User.objects.filter(followers=request.user).count()
    return render(request, "network/profile.html", {"followers_count": followers_count, "following_count": following_count})