from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from .forms import UserSignUpForm, UserSignInForm


def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(data = request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account is created successfully. You can now sign in!")
            return redirect('users-signin')
        else:
            messages.error(request, f"Error occured while signing up!")
    else:
        form = UserSignUpForm()
    context = {'form': form,
               'title': 'Sign Up',
               'active': 'signup'}
    return render(request, 'Users/signup.html', context = context)


def signin(request):
    if request.method == 'POST':
        form = UserSignInForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You are succesfully signed in!")
            return redirect('website-home')
        else:
            messages.error(request, "Error occured while signing in!")
    else:
        form = UserSignInForm()
    context = {'form': form,
               'title': 'Sign In',
               'active': 'signin'}
    return render(request, 'Users/signin.html', context = context)


def signout(request):
    logout(request)
    messages.success(request, "You are succesfully signed out!")
    return redirect('website-home')