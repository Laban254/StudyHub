from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views import View
from .models import *
from .forms import *
from django.contrib import messages
from email.mime import audio
from django.core.paginator import Paginator
# from schedule.models import Calendar, Event


import sweetify
# For APIs
import requests


class RegistrationView(SuccessMessageMixin, FormView):
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('studyApp:login')
    success_message = "Account for %(username)s created successfully"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')


from django.db.models import Q

from django.contrib import messages


@login_required
def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, "Note added successfully.")
            return redirect('studyApp:notes')
    else:
        form = NotesForm()

    notes_list = Notes.objects.filter(user=request.user)
    
    query = request.GET.get('q')
    if query:
        notes_list = notes_list.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    paginator = Paginator(notes_list, 8)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Check if there are any reminders
    has_reminders = any(note.reminder for note in notes_list)

    context = {
        'form': form,
        'page_obj': page_obj,
        'total_notes_count': notes_list.count(),
        'has_reminders': has_reminders,  # Pass the flag to the template
    }
    return render(request, 'notes.html', context)

class NotesDetailView(generic.DetailView):
    model = Notes

@login_required
def delete_note(request, pk):
    note = Notes.objects.get(id=pk)
    # Check if the note belongs to the current user before deleting
    if note.user == request.user:
        note.delete()
        sweetify.success(request, "Note deleted successfully", button='OK')
        # sweetify.toast(request, 'note deleted successfully')
    else:
        sweetify.error(request, "You are not authorized to delete this note")
    return redirect('studyApp:notes')

@login_required
def edit_note(request, pk):
    note = get_object_or_404(Notes, id=pk)
    if note.user != request.user:
        return redirect('studyApp:notes')

    if request.method == 'POST':
        form = NotesForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            sweetify.success(request, "Note updated successfully")
            return redirect('studyApp:notes')
    else:
        form = NotesForm(instance=note)

    context = {
        'form': form,
        'note': note,
    }
    return render(request, 'edit_note.html', context)

def edit_reminder(request, note_id):
    if request.method == 'POST':
        note = Notes.objects.get(pk=note_id)
        new_reminder = request.POST.get('reminder')
        note.reminder = new_reminder
        note.save()
        messages.success(request, 'Reminder updated successfully.')
        return redirect('studyApp:notes')
    else:
        # Handle GET request if needed
        pass

def delete_reminder(request, note_id):
    if request.method == 'POST':
        note = Notes.objects.get(pk=note_id)
        note.reminder = None  # Remove the reminder
        note.save()
        messages.success(request, 'Reminder deleted successfully.')
        return redirect('studyApp:notes')
    else:
        # Handle GET request if needed
        pass


from django.shortcuts import get_object_or_404
@login_required
def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.user = request.user
            homework.save()

            # # Attempt to get the first calendar object, or create one if it doesn't exist
            # calendar = Calendar.objects.first()
            # if calendar is None:
            #     calendar = Calendar.objects.create(name='Default Calendar')

            # # Create an event in the calendar for the homework deadline
            # event = Event(
            #     calendar=calendar,
            #     title=homework.title,
            #     description=homework.description,
            #     start=homework.due,  # Assuming your Homework model has a 'due' field
            #     end=homework.due,    # Assuming you want the event to last for a single day
            # )
            # event.save()

            messages.success(request, "Homework added successfully")
            return redirect('studyApp:homework')
        else:
            error_message = "Failed to add homework: " + form.errors.as_text()
            messages.error(request, error_message)
    else:
        form = HomeworkForm()

    homeworks = Homework.objects.filter(user=request.user)
    unfinished_homeworks = homeworks.filter(is_finished=False)
    paginator = Paginator(homeworks, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'homeworks': homeworks,
        'unfinished_homeworks': unfinished_homeworks,
        'form': form,
        'page_obj': page_obj,
        'total_homework_count': homeworks.count(),
    }
    return render(request, 'homework.html', context)




class HomeworkDetailView(generic.DetailView):
    model = Homework


from django.utils.safestring import mark_safe

import json

@login_required
def calendar_view(request):
    # Query homework deadlines for the current user
    homework_deadlines = Homework.objects.filter(user=request.user)

    # Prepare events for the calendar
    events = []
    for homework in homework_deadlines:
        events.append({
            'title': homework.title,
            'start': homework.due.strftime('%Y-%m-%d'),  # Format the due date as required by FullCalendar
            # Add more event properties as needed
        })

    # Pass events to the template
    context = {
        'events': mark_safe(json.dumps(events))  # Mark the events as safe to prevent HTML escaping
    }
    return render(request, 'calendar.html', context)


@login_required
def update_homework(request, pk=None):
    # Retrieve the homework object from the database
    homework = get_object_or_404(Homework, id=pk)

    # Check if the current user is the owner of the homework
    if homework.user != request.user:
        return redirect('studyApp:homework')

    if request.method == 'POST':
        # Create the form instance with the POST data and the homework instance
        form = HomeworkForm(request.POST, instance=homework)
        if form.is_valid():
            # Save the form to update the homework object
            form.save()
            messages.success(request, "Homework updated successfully")
            return redirect('studyApp:homework')
        else:
            messages.error(request, "Failed to update homework. Please correct the errors.")
    else:
        # Create the form instance with the homework instance (no POST data)
        form = HomeworkForm(instance=homework)

    context = {
        'form': form,
        'homework': homework,
    }
    return render(request, 'update_homework.html', context)

@login_required
def delete_homework(request, pk):
    homework = get_object_or_404(Homework, id=pk)
    homework.delete()
    sweetify.success(request, "Homework deleted successfully")
    return redirect('studyApp:homework')

#TODO
@login_required
def todo(request):
    if request.method == 'POST':
        form= TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                # If the checkbox has been clicked
                if finished == 'on':
                    finished = True
                # if the checkbox has not been clicked
                else:
                    finished = False
            except:
                finished = False
            # List all the form fields as POST requests
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todos.save()
        messages.success(request, f"todo added successfully")
    else:
        form = TodoForm()
    todos = Todo.objects.filter(user=request.user)
    if len(todos) == 0:
        todos_done = True
    # if the number of todos is 1 or more then they are incomplete
    else:
        todos_done = False
    context={
        'todos':todos,
        'todos_done':todos_done,
        'form':form,
    }
    return render(request, 'todo.html', context)

@login_required
def update_todo(request, pk):
    todo = Todo.objects.get(id=pk)
    # if the status checkbox is ticked then the assignment is completed
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('studyApp:todo')

def delete_todo(request, pk):
    # Use the correct model name and access its objects
    todo_instance = get_object_or_404(Todo, id=pk)
    todo_instance.delete()
    return redirect('studyApp:todo')

#BOOKS
@login_required
def books(request):
    form = BookSearchForm()
    if request.method == 'POST':
        form = BookSearchForm(request.POST)
        # text is the field from BookSearchForm where user writes the book they want to search
        text = request.POST['text']
        # Url to the googlebooks API
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        # initiates the requests
        r = requests.get(url)
        # we get the result(answer) from the requests in json format
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
                # 'link':answer['items'][i]['volumeInfo'].get('link')
            }
            result_list.append(result_dict)
            context = {
                'form':form,
                'result_list':result_list
            }
        return render(request, 'books.html',  context)
    else:
        form = BookSearchForm()
    context = {
        'form':form,
    }
    return render(request, 'books.html',  context)

# DICTIONARY
@login_required
def dictionary(request):
    form = DictionarySearchForm()
    if request.method == 'POST':
        form = DictionarySearchForm(request.POST)
        # text is the field from DictionarySearchForm where user writes the book they want to search
        text = request.POST['text']
        # Url to the Wikipedia API
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        # initiates the requests
        r = requests.get(url)
        # we get the result(answer) from the requests in json format
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms
            }

        except:
            context = {
                'form':form,
                'input':''
            }
        return render(request, 'dictionary.html', context)
    else:
        form = DictionarySearchForm() 
        context = {
            'form':form,
        }
    return render(request, 'dictionary.html', context)

