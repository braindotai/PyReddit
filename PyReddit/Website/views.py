from django.shortcuts import render

posts = [
    {'title': 'Blog 1',
    'author': 'Rishik',
    'description': 'In this blog we will cover how to improve performance in loops',
    'date_posted': 'August 27, 2019'},
    
    {'title': 'Blog 2',
     'author': 'Rudra',
     'description': 'Comparing inference performance of different deep learning frameworks',
     'date_posted': 'August 29, 2019'}
]

def home(request):
    context = {'posts': posts}
    return render(request, 'Website/home.html', context = context)