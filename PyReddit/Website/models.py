from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length = 50)
    description = models.CharField(max_length = 300)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self, **kwargs):
        return reverse('website-postdetail', kwargs = {'pk': self.pk})