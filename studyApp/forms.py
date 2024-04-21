from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from dataclasses import fields
from .models import *
from django.forms import widgets

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1', 'password2' ]


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'description']
