from django.shortcuts import render
from .models import Post

def home(request):
    context = {'posts': Post.objects.all(),
               'active': 'home'}
    return render(request, 'Website/home.html', context = context)