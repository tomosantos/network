
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.new_post, name="newPost"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("follow/", views.follow, name="follow"),
    path("unfollow/", views.unfollow, name="unfollow"),
    path("following/", views.following, name="following"),
    path("like/<int:post_id>", views.like, name="like"),
    path("unlike/<int:post_id>", views.unlike, name="unlike"),
    path("edit/<int:post_id>", views.edit, name="edit")
]
