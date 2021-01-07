from django import forms
from django.contrib.auth.models import User
from .models import Account
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserSignUpForm(UserCreationForm):
    first_name = forms.CharField(required = False, widget = forms.TextInput(attrs = {'placeholder': 'First Name'}))
    last_name = forms.CharField(required = False, widget = forms.TextInput(attrs = {'placeholder': 'Last Name'}))
    username = forms.CharField(required = False, widget = forms.TextInput(attrs = {'placeholder': 'Username'}), help_text = "Minimum 5 characters")
    email = forms.EmailField(required = False, widget = forms.EmailInput(attrs = {'placeholder': 'Email'}))
    password1 = forms.CharField(required = False, widget = forms.PasswordInput(attrs = {'placeholder': 'Password'}), help_text = 'Minimum 8 characters')
    password2 = forms.CharField(required = False, widget = forms.PasswordInput(attrs = {'placeholder': 'Confirm Password'}), help_text = 'Retype password')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        if len(username) == 0:
            raise forms.ValidationError('Username is required!')
        if len(username) < 5:
            raise forms.ValidationError('Username should contains at least 5 characters')
        if any(map(lambda symbol: symbol in username, ['!', '@', '#', '$' '%', '^', '&', '*', '(', ')'])):
            raise forms.ValidationError("Symbol '!', '@', '#', '$' '%', '^', '&', '*', '(' and ')' should not be used")
        return username

    def clean_first_name(self, *args, **kwargs):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) == 0:
            raise forms.ValidationError('First name is required!')
        if len(first_name) > 30:
            raise forms.ValidationError('First name should not contain more than 30 characters!')
        return first_name

    def clean_last_name(self, *args, **kwargs):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) > 30:
            raise forms.ValidationError('Last name should not contain more than 30 characters!')
        return last_name

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        if len(email) == 0:
            raise forms.ValidationError('Email is required!')
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError(f'Account with email "{email}" already exists!')
        return email
    
    def clean_password1(self, *args, **kwargs):
        password1 = self.cleaned_data.get('password1')
        if len(password1) == 0:
            raise forms.ValidationError('Password is required!')
        if len(password1) < 8:
            raise forms.ValidationError('Password should contains at least 8 characters!')
        return password1

    def clean_password2(self, *args, **kwargs):
        password2 = self.cleaned_data.get('password2')
        if len(password2) == 0:
            raise forms.ValidationError('Confirm Password is required!')
        if password2 != self.cleaned_data.get('password1'):
            raise forms.ValidationError('Password did not match!')
        if len(password2) < 8:
            raise forms.ValidationError('Password should contains at least 8 characters!')
        return password2
    

class UserSignInForm(AuthenticationForm):
    username = forms.CharField(required = False, widget = forms.TextInput(attrs = {'placeholder': 'Username or Email'}))
    password = forms.CharField(required = False, widget = forms.PasswordInput(attrs = {'placeholder': 'Password'}))
    
    class Meta:
        model = User
        fields = ('username', 'password')
    
    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        if len(username) == 0:
            raise forms.ValidationError('Username or Email is required')
        if '@' in username:
            user = User.objects.filter(email = username)
            if user.exists():
                return user.first().username
            else:
                raise forms.ValidationError(f'Account with email "{username}" does not exist!')
        else:
            user = User.objects.filter(username = username)
            if user.exists():
                return user.first().username
            else:
                raise forms.ValidationError(f'Account with username "{username}" does not exist!')
        return username
    
    def clean_password(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        if len(password) == 0:
            raise forms.ValidationError('Password is required')
        user = User.objects.filter(username = self.cleaned_data.get('username'))
        if user.exists():
            if not user.first().check_password(password):
                raise forms.ValidationError(f'Password is invalid!')
        return password



class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required = False)
    last_name = forms.CharField(required = False)
    username = forms.CharField(required = False)
    email = forms.EmailField(required = False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['image']



# class PasswordResetForm(forms.ModelForm):
#     email = forms.EmailField(required = False, widget = forms.TextInput(attrs = {'placeholder': 'Email of the account'}))

#     class Meta:
#         model = User
#         fields = ["email"]
    
#     def clean_email(self, *args, **kwargs):
#         email = self.cleaned_data.get('email')
#         if len(email) == 0:
#             raise forms.ValidationError('Email is required to reset forgotten password!')
        
#         user = User.objects.filter(email = email)
#         if not user.exists():
#             raise forms.ValidationError(f'Account with email "{email}" does not exist!')
#         return email