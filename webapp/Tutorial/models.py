from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

class ForumPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    postTitle = models.CharField(max_length = 100)
    postBody = models.CharField(max_length = 1000)
    postDate = models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.postTitle

