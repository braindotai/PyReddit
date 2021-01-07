from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name = 'users-signup'),
    path('signin/', views.signin, name = 'users-signin'),
    path('signout/', views.signout, name = 'users-signout'),
    path('account/', views.account, name = 'users-account'),
    # path('password-reset/', PasswordResetView.as_view(template_name = "Users/password_reset.html"), name = "password-reset"),
    # path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name = "Users/password_reset_confirm.html"), name = "password-reset-confirm"),
    # path('password-reset/done/', PasswordResetDoneView.as_view(template_name = "Users/password_reset_done.html"), name = "password-reset-done")
]