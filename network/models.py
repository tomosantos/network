from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="author")
    content = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Post {self.id} made by {self.user} on {self.timestamp.strftime('%d %b %Y %H:%M:%S')}"
    
    
class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="user_who_is_following")
    user_follower = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="user_who_is_being_followed")

    def __str__(self):
        return f"{self.user} is following {self.user_follower}."

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_like")
    

    def __str__(self):
        return f'{self.user} liked {self.post}'
