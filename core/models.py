from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    body = models.TextField(max_length=140)
    no_of_likes = models.IntegerField(default=0)
    no_of_dislikes = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now)
    

