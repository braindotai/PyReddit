from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name = 'users-signup'),
    path('signin/', views.signin, name = 'users-signin'),
    path('signout/', views.signout, name = 'users-signout'),
    path('account/', views.account, name = 'users-account')
] 