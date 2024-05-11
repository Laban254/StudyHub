from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'studyApp'

urlpatterns = [
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
    
     path('notes/', notes, name="notes"),
     path('edit-note/<int:pk>/', edit_note, name='edit_note'),
    # this path takes one to a specific note and delete's it
    path('delete_note/<int:pk>/', delete_note, name="delete_note"),
    # this path references a generic view hence '.as_view'
    path('notes_view/<int:pk>/', NotesDetailView.as_view(), name="notes_detail"),
    path('edit_reminder/<int:note_id>/', edit_reminder, name='edit_reminder'),
    path('delete_reminder/<int:note_id>/', delete_reminder, name='delete_reminder'),


    path('homework/', homework, name="homework"),
    path('edit_homework/<int:pk>', update_homework, name="edit_homework"),
    path('delete_homework/<int:pk>/', delete_homework, name="delete_homework"),
    path('homework_view/<int:pk>/', HomeworkDetailView.as_view(), name="homework_detail"),
    path('calendar_view/', calendar_view, name="calendar_view"),

    path('todo/', todo, name="todo"),
    path('update_todo/<int:pk>', update_todo, name="update_todo"),
    path('delete_todo/<int:pk>/', delete_todo, name="delete_todo"),



    path('books/', books, name="books"),

    path('dictionary/', dictionary, name='dictionary'),

   
    
]
