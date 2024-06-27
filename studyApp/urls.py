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

    path('about/', About.as_view(), name="about"),
    
     path('notes/', notes, name="notes"),
     path('edit-note/<int:pk>/', edit_note, name='edit_note'),
    # this path takes one to a specific note and delete's it
    path('delete_note/<int:pk>/', delete_note, name="delete_note"),
    # this path references a generic view hence '.as_view'
    path('notes_view/<int:pk>/', notes_detail, name="notes_detail"),
    path('edit_reminder/<int:note_id>/', edit_reminder, name='edit_reminder'),
    path('delete_reminder/<int:note_id>/', delete_reminder, name='delete_reminder'),

    # path('notes/', share_notes, name='share_note'),
    path('shared/notes/received/', shared_notes_received, name='shared_notes_received'),
    path('shared/notes/sent/', shared_notes_sent, name='shared_notes_sent'),

    path('toggle_favorite/<int:note_id>/', toggle_favorite, name='toggle_favorite'),

    path('homework/', homework, name="homework"),
    path('edit_homework/<int:pk>', update_homework, name="edit_homework"),
    path('delete_homework/<int:pk>/', delete_homework, name="delete_homework"),
    path('homework_view/<int:pk>/', HomeworkDetailView.as_view(), name="homework_detail"),
    path('calendar_view/', calendar_view, name="calendar_view"),

    path('', task_list, name='task_list'),
    path('task/create/', task_create, name='task_create'),
    path('task/<int:task_id>/edit/', task_update, name='task_update'),
    path('task/<int:task_id>/delete/', task_delete, name='task_delete'),


    path('books/', books, name="books"),

    path('dictionary/', dictionary, name='dictionary'),

   
    
]
