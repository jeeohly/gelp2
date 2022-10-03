from django.db import models
from django.contrib.auth import get_user_model
from traitlets import default

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank = True)
    rating = models.IntegerField(default = 0)

    def __str__(self):
        return self.user.username

