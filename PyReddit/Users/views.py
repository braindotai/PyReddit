from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
# from django.contrib.auth.views import PasswordResetView
from .forms import UserSignUpForm, UserSignInForm, UserUpdateForm, ProfileUpdateForm


def signup(request):
    if request.method == 'POST':
        print(request.POST)
        
        form = UserSignUpForm(data = request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account is created successfully!")
            return redirect('website-home')
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
            if request.GET.get('next') is None:
                return redirect('website-home')
            return redirect(request.GET.get('next'))
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


@login_required
def account(request):
    if request.method == 'POST':
        info_form = UserUpdateForm(request.POST, instance = request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                         request.FILES,
                                         instance = request.user.account)
        if info_form.is_valid() and profile_form.is_valid():
            info_form.save()
            profile_form.save()
            messages.success(request, "Your account has been updated successfully!")
            return redirect('users-account')
    else:
        info_form = UserUpdateForm(instance = request.user)
        profile_form = ProfileUpdateForm(instance = request.user.account)

    context = {'title': 'Account',
               'active': 'account',
               'info_form': info_form,
               'profile_form': profile_form}
    return render(request, 'Users/account.html', context = context)


# class passwordreset(PasswordResetView):
#     form_class = PasswordResetForm
#     template_name = "Users/password_reset.html"