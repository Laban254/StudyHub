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



class TaskForm(forms.ModelForm):
    # tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control bg-light', 'placeholder': 'Enter tags (comma-separated)'}), required=False)

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'category', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control bg-light', 'placeholder': 'Enter title'}),
            'description': forms.Textarea(attrs={'class': 'form-control bg-light', 'placeholder': 'Enter description'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control bg-light', 'type': 'date'}),
            'priority': forms.Select(attrs={'class': 'form-control bg-light'}),
            'category': forms.Select(attrs={'class': 'form-control bg-light'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    # def save(self, commit=True):
    #     task = super().save(commit=False)
    #     if commit:
    #         task.save()  # Save the task first to get an ID
            
    #         # Handle tags after task is saved
    #         tags_str = self.cleaned_data['tags']
    #         if tags_str:
    #             tags_list = [tag.strip() for tag in tags_str.split(',')]
    #             for tag_name in tags_list:
    #                 tag, created = Tag.objects.get_or_create(name=tag_name)
    #                 task.tags.add(tag)
            
    #         self.save_m2m()  # Save many-to-many relationships after main object is saved
    #     return task



class BookSearchForm(forms.Form):
    text = forms.CharField(max_length=255, label="Search for books")

class DictionarySearchForm(forms.Form):
    text = forms.CharField(max_length=255, label="Search for words")

