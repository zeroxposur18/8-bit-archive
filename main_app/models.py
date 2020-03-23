from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

