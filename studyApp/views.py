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
from django.views.decorators.http import require_POST
from actstream.models import Action
from django.db.models import Q

from django.contrib import messages

from django.http import HttpResponseBadRequest
# from schedule.models import Calendar, Event


import sweetify
# For APIs
import requests

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'about.html')

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





@login_required
def notes(request):
    create_notes_form = NotesForm()
    share_note_form = ShareNoteForm()

    if request.method == 'POST':
        if 'create_note' in request.POST:
            return handle_create_notes(request, create_notes_form)
        elif 'share_note' in request.POST:
            return handle_share_notes(request, share_note_form)
        else:
            return HttpResponseBadRequest("Invalid POST request")

    # For GET requests, return the forms along with other necessary context
    notes_list = Note.objects.filter(user=request.user)
    shared_notes_sent = SharedNote.objects.filter(shared_by=request.user)
    shared_notes_received = SharedNote.objects.filter(shared_with=request.user)
    favorite_notes = notes_list.filter(favorite=True)
    activities = Action.objects.all()[:10]
    
    # Filter notes by search query if present
    query = request.GET.get('q')
    if query:
        notes_list = notes_list.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # Sort notes based on sorting parameter
    sort_by = request.GET.get('sort_by')
    if not sort_by:
        # Set default sorting to arrange notes by time created with the newest first
        notes_list = notes_list.order_by('-created_at')
    elif sort_by == 'title':
        notes_list = notes_list.order_by('title')
    elif sort_by == '-title':
        notes_list = notes_list.order_by('-title')
    elif sort_by == 'date_created':
        notes_list = notes_list.order_by('created_at')
    elif sort_by == '-date_created':
        notes_list = notes_list.order_by('-created_at')

    paginator = Paginator(notes_list, 8)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    has_reminders = any(note.reminder for note in notes_list)

    context = {
        'create_notes_form': create_notes_form,
        'share_note_form': share_note_form,
        'page_obj': page_obj,
        'total_notes_count': notes_list.count(),
        'has_reminders': has_reminders,
        'shared_notes_sent': shared_notes_sent,
        'shared_notes_received': shared_notes_received,
        'favorite_notes': favorite_notes,
        'activities': activities,
    }
    return render(request, 'notes.html', context)


def handle_create_notes(request, form):
    form = NotesForm(request.POST)
    if form.is_valid():
        note = form.save(commit=False)
        note.user = request.user
        note.save()
        messages.success(request, "Note added successfully.")
    return redirect('studyApp:notes')

def handle_share_notes(request, form):
    form = ShareNoteForm(request.POST)
    if form.is_valid():
        note = form.cleaned_data['note']
        users = form.cleaned_data['users']
        current_user = request.user
        for user in users:
            shared_note = SharedNote.objects.create(
                note=note,
                shared_by=current_user
            )
            shared_note.shared_with.set([user])
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)


# class NotesDetailView(generic.DetailView):
#     model = Note
#     template_name = 'studyApp/notes_detail.html'

def notes_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'notes_detail.html', {'note': note})

@require_POST
def toggle_favorite(request, note_id):
    note = Note.objects.get(pk=note_id)
    note.favorite = not note.favorite
    note.save()

    if note.favorite:
        messages.info(request, f'Note "{note.title}" added to favorites.')
    else:
        messages.info(request, f'Note "{note.title}" removed from favorites.')

    return redirect('studyApp:notes')


@login_required
def delete_note(request, pk):
    note = Note.objects.get(id=pk)
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
    note = get_object_or_404(Note, id=pk)
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
        note = Note.objects.get(pk=note_id)
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
        note = Note.objects.get(pk=note_id)
        note.reminder = None  # Remove the reminder
        note.save()
        messages.success(request, 'Reminder deleted successfully.')
        return redirect('studyApp:notes')
    else:
        # Handle GET request if needed
        pass


from django.http import JsonResponse

from django.http import JsonResponse

# @login_required
# def share_notes(request):
#     if request.method == 'POST':
#         form = ShareNoteForm(request.POST)
#         if form.is_valid():
#             note = form.cleaned_data['note']
#             users = form.cleaned_data['users']
#             current_user = request.user
#             for user in users:
#                 shared_note = SharedNote.objects.create(
#                     note=note,
#                     shared_with=user,
#                     shared_by=current_user
#                 )
#             return JsonResponse({'success': True})  # Return a JSON response indicating success
#         else:
#             return JsonResponse({'success': False, 'errors': form.errors}, status=400)  # Return errors if form is invalid
#     elif request.method == 'GET':
#         form = ShareNoteForm()  # Create an instance of the form
#         return JsonResponse({'form': form.as_json()})  # Return the form data as JSON


@login_required
def shared_notes_received(request):
    shared_notes_received = SharedNote.objects.filter(shared_with=request.user)
    data = [
        {
            'note': shared_note.note.title,
            'shared_by': shared_note.shared_by.username,
            'shared_date': shared_note.shared_date.strftime('%Y-%m-%d %H:%M:%S')  # Format the date as needed
        }
        for shared_note in shared_notes_received
    ]
    return JsonResponse(data, safe=False)

@login_required
def shared_notes_sent(request):
    shared_notes_sent = SharedNote.objects.filter(shared_by=request.user)
    data = [
        {
            'note': shared_note.note.title,
            'shared_with': shared_note.shared_with.username,
            'shared_date': shared_note.shared_date.strftime('%Y-%m-%d %H:%M:%S')  # Format the date as needed
        }
        for shared_note in shared_notes_sent
    ]
    return JsonResponse(data, safe=False)

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

# todo
@login_required
def todo(request):
    if request.method == 'POST' and not request.is_ajax():
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                finished = True if finished == 'on' else False
            except KeyError:
                finished = False
            todos = Todo(
                user=request.user,
                title=request.POST['title'],
                is_finished=finished
            )
            todos.save()
            messages.success(request, "Todo added successfully")
        else:
            messages.error(request, "Error adding todo")
    else:
        form = TodoForm()

    todos = Todo.objects.filter(user=request.user)
    todos_done = len(todos) == 0

    context = {
        'todos': todos,
        'todos_done': todos_done,
        'form': form,
    }
    return render(request, 'todo.html', context)

@login_required
def update_todo_status(request):
    if request.method == 'POST':
        todo_id = request.POST.get('todo_id')
        is_checked = request.POST.get('is_checked') == 'true'
        
        try:
            todo = Todo.objects.get(id=todo_id, user=request.user)
            todo.is_finished = is_checked
            todo.save()
            return JsonResponse({'status': 'success'})
        except Todo.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Todo not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def delete_todo(request, pk):
    todo_instance = get_object_or_404(Todo, id=pk, user=request.user)
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

