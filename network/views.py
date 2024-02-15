from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json

from .models import Follow, Like, Post, User


def index(request):
    posts = Post.objects.all().order_by("id").reverse()

    # Paginator
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_posts = paginator.get_page(page_number)

    # Likes
    likes = Like.objects.all()
    posts_liked = []

    try:
        for like in likes:
            if like.user.id == request.user.id:
                posts_liked.append(like.post.id)
    except:
        posts_liked = []

    return render(request, "network/index.html", {
        "posts": posts,
        "page_posts": page_posts,
        "posts_liked": posts_liked,
    })


def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(user=user).order_by("id").reverse()

    # Following & Followers
    following = Follow.objects.filter(user=user)
    followers = Follow.objects.filter(user_follower=user)

    try:
        verify_follow = followers.filter(
            user=User.objects.get(pk=request.user.id))

        if len(verify_follow) != 0:
            isFollowing = True
        else:
            isFollowing = False
    except:
        isFollowing = False
        
    # Likes
    likes = Like.objects.all()
    posts_liked = []

    try:
        for like in likes:
            if like.user.id == request.user.id:
                posts_liked.append(like.post.id)
    except:
        posts_liked = []

    # Paginator
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_posts = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "posts": posts,
        "page_posts": page_posts,
        "username": user.username,
        "following": following,
        "followers": followers,
        "isFollowing": isFollowing,
        "user_profile": user,
        "posts_liked": posts_liked,
    })


# Follow & Unfollow
def follow(request):
    follow_user = request.POST["followUser"]
    currentUser = User.objects.get(pk=request.user.id)
    follow_userData = User.objects.get(username=follow_user)

    f = Follow(user=currentUser, user_follower=follow_userData)
    f.save()

    user_id = follow_userData.id

    return HttpResponseRedirect(reverse("profile", kwargs={'user_id': user_id}))


def unfollow(request):
    follow_user = request.POST["followUser"]
    currentUser = User.objects.get(pk=request.user.id)
    follow_userData = User.objects.get(username=follow_user)

    f = Follow.objects.get(user=currentUser, user_follower=follow_userData)
    f.delete()

    user_id = follow_userData.id

    return HttpResponseRedirect(reverse("profile", kwargs={'user_id': user_id}))


# Following
def following(request):
    currentUser = User.objects.get(pk=request.user.id)
    following_users = Follow.objects.filter(user=currentUser)

    posts = Post.objects.all().order_by("id").reverse()

    following_posts = []

    for post in posts:
        for user in following_users:
            if user.user_follower == post.user:
                following_posts.append(post)
                
    # Likes
    likes = Like.objects.all()
    posts_liked = []

    try:
        for like in likes:
            if like.user.id == request.user.id:
                posts_liked.append(like.post.id)
    except:
        posts_liked = []

    # Paginator
    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get("page")
    page_posts = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page_posts": page_posts,
        "posts_liked": posts_liked,
    })


# Edit
def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Post.objects.get(pk=post_id)
        edit_post.content = data["content"]
        edit_post.save()

        return JsonResponse({"message": "Change sucessful", "data": data["content"]})

# Like & Unlike
def like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)

    l = Like(user=user, post=post)
    l.save()
    
    post.likes_count += 1
    post.save()

    return JsonResponse({"message": "Like added!", "likes_count": post.likes_count})


def unlike(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)

    l = Like.objects.filter(user=user, post=post)
    l.delete()
    
    if post.likes_count > 0:
        post.likes_count -= 1
        post.save()

    return JsonResponse({"message": "Like removed!", "likes_count": post.likes_count})
    

# New Post
def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        user = User.objects.get(pk=request.user.id)

        post = Post(content=content, user=user)
        post.save()

        return HttpResponseRedirect(reverse('index'))


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
