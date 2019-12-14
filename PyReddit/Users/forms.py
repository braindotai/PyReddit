from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length = 30, widget = forms.TextInput(attrs = {'class': 'input', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length = 30, widget = forms.TextInput(attrs = {'class': 'input', 'placeholder': 'Last Name'}))
    username = forms.CharField(max_length = 30, widget = forms.TextInput(attrs = {'class': 'input', 'placeholder': 'Username'}), help_text = 'Minimum 5 characters')
    email = forms.EmailField(widget = forms.EmailInput(attrs = {'class': 'input', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget = forms.PasswordInput(attrs = {'class': 'input', 'placeholder': 'Password'}), help_text = 'Minimum 8 characters')
    password2 = forms.CharField(widget = forms.PasswordInput(attrs = {'class': 'input', 'placeholder': 'Confirm Password'}), help_text = 'Retype password')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit = True):
        user = super(UserSignUpForm, self).save(commit = False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.full_name = self.cleaned_data['first_name'] + ' ' + self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.password = self.cleaned_data['password1']

        if commit:
            user.save()
        return user
    
    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        if len(username) < 5:
            raise forms.ValidationError('Username should contains at least 5 characters')
        return username
    
    def clean_password(self, *args, **kwargs):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError('Password should contains at least 8 characters!')
        return password1
    
    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError(f'Account with email "{email}" already exists!')
        return email


class UserSignInForm(AuthenticationForm):
    username = forms.CharField(widget = forms.TextInput(attrs = {'class': 'input', 'placeholder': 'Username or Email'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs = {'class': 'input', 'placeholder': 'Password'}))
    
    class Meta:
        model = User
        fields = ('username', 'password')
    
    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
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
        user = User.objects.filter(username = self.cleaned_data.get('username'))
        if user.exists():
            if not user.first().check_password(password):
                raise forms.ValidationError(f'Password is invalid!')
        return password

