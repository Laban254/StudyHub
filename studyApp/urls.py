from django.urls import path
from django.contrib.auth import views as auth_views
from .views import HomeView, RegistrationView

app_name = 'studyApp'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_done.html'), name='password_reset_complete'),
]
