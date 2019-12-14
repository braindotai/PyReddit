from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name = 'users-signup'),
    path('signin/', views.signin, name = 'users-signin'),
    path('signout/', views.signout, name = 'users-signout'),
] 