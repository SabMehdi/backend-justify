from django.db import models
from django.contrib.auth.models import User

class WordCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    class Meta:
        app_label = 'server'  