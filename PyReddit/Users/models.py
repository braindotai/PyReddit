from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Account(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(default = 'default.png', upload_to = 'profiles')

    def __str__(self):
        return f"Account for {self.user.username}"
    
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        img.thumbnail((300, 300), Image.ANTIALIAS)
        img.save(self.image.path)
