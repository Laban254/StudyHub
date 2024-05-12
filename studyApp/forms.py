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
        model = Note
        fields = ['title', 'description', 'reminder']
        widgets = {'reminder': forms.DateInput(attrs={'type': 'date'})}


class ShareNoteForm(forms.Form):
    note = forms.ModelChoiceField(queryset=Note.objects.all())
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all())


# This is a class of DateInput to show a widget of a calender when adding dates in a form
class DateInput(forms.DateInput):
    input_type = 'date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['subject', 'title', 'description', 'due', 'is_finished']
        widgets = {'due': forms.DateInput(attrs={'type': 'date'})}

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'is_finished']

class YoutubeSearchForm(forms.Form):
    text = forms.CharField(max_length=255, label="Search youtube video")


class BookSearchForm(forms.Form):
    text = forms.CharField(max_length=255, label="Search for books")

class DictionarySearchForm(forms.Form):
    text = forms.CharField(max_length=255, label="Search for words")

