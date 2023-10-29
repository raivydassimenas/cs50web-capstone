import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator

from .models import User, Post


def index(request):

    new_post = request.user.is_authenticated
    all_posts = Post.objects.all().order_by("-created")
    for post in all_posts:
        post.can_like = request.user != post.author and request.user not in post.likes.all()
        post.can_unlike = request.user in post.likes.all()

    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "network/index.html", { "new_post": new_post, "page": page })


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
    all_posts = Post.objects.all().order_by("-created")
    return JsonResponse([post.serialize() for post in all_posts], safe=False)

@login_required
def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    followers_count = user.followers.all().count()
    following_count = User.objects.filter(followers=user).count()
    posts = Post.objects.filter(author=user).order_by("-created")
    same_user = request.user.id == user_id
    follow = user.followers.filter(pk=request.user.id).exists()
    return render(request, "./network/profile.html", {"user": user, "followers_count": followers_count, "following_count": following_count, "posts": posts, "same_user": same_user, "follow": follow}, status=200)

@login_required
def follow(request, target_user_id):
    try:
        target_user = User.objects.get(pk=target_user_id)
        source_user = User.objects.get(pk = request.user.id)
        target_user.followers.add(source_user)
        return HttpResponseRedirect(reverse("profile", args=(request.user.id,)))
    except target_user.DoesNotExist:
        return render(request, "./network/profile.html", {"error": "Target user does not exist"}, status=404)
    except Exception as e:
        return render(request, "./network/profile.html", {"error": str(e)}, status=400)
    
@login_required
def unfollow(request, target_user_id):
    try:
        target_user = User.objects.get(pk=target_user_id)
        source_user = User.objects.get(pk = request.user.id)
        target_user.followers.remove(source_user)
        return HttpResponseRedirect(reverse("profile", args=(request.user.id, )))
    except target_user.DoesNotExist:
        return JsonResponse({"error": "Target user does not exist"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@login_required
def following(request):
    users_following = request.user.following.all()
    posts_following = Post.objects.filter(author__in=users_following).order_by("-created")
    paginator = Paginator(posts_following, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "./network/following.html", {"page": page})

@login_required
@csrf_exempt
@require_http_methods(["PUT"])
def update_post(request, post_id):
    post = Post.objects.filter(pk=post_id)

    if not post.exists() or post.first().author != request.user:
        return JsonResponse({"error": "Cannot update post"}, status=403)

    post = post.first()
    data = json.loads(request.body)
    post.body = data["body"]
    post.save()

    return JsonResponse({"message": "Post updated successfully"}, status=200)

    
@login_required
@csrf_exempt
def like(request, post_id):
    posts = Post.objects.filter(pk=post_id)

    if not posts.exists():
        return JsonResponse({"error": "Post does not exist"}, status=404)
        
    post = posts.first()

    if post.author == request.user:
        return JsonResponse({"error": "You cannot like your own post"}, status=403)

    if request.user in post.likes.all():
        return JsonResponse({"error": "You already liked this post"}, status=403)

    post.likes.add(request.user)
    post.save()
    return HttpResponseRedirect(reverse("index"))


@login_required
@csrf_exempt
def unlike(request, post_id):
    posts = Post.objects.filter(pk=post_id)

    if not posts.exists():
        return JsonResponse({"error": "Post does not exist"}, status=404)

    post = posts.first()

    if post.author == request.user:
        return JsonResponse({"error": "You cannot unlike your own post"}, status=403)

    if request.user not in post.likes.all():
        return JsonResponse({"error": "You have not liked this post"}, status=403)

    post.likes.remove(request.user)
    post.save()
    return HttpResponseRedirect(reverse("index"))