from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic
from django.views import View
from .models import *
from .forms import *
from django.contrib import messages
from email.mime import audio
#YouTube Search Library
from youtubesearchpython import VideosSearch
# For APIs
import requests
# Wikipedia API
import wikipedia

class RegistrationView(SuccessMessageMixin, FormView):
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('studyApplogin')
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


# NOTES
@login_required
def notes(request):
    form = NotesForm()
    # Create Notes Form
    if request.method == 'POST':
        form= NotesForm(request.POST)
        if form.is_valid():
            # List out the form fields as POST requests
            notes = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
        messages.success(request, f"Notes added successfully")    
    else:
        form=NotesForm()
    # The notes will be filtered and displayed based on the current logged in user
    notes = Notes.objects.filter(user=request.user)
    context={
        'form':form,
        'notes':notes,
    }
    return render(request, 'notes.html', context)

class NotesDetailView(generic.DetailView):
    model = Notes

@login_required
def delete_note(request, pk):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')


# HOMEWORK
@login_required
def homework(request):
    if request.method == 'POST':
        form= HomeworkForm(request.POST)
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
            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
            )
            homeworks.save()
        messages.success(request, f"Homework added successfully")
    else:
        form = HomeworkForm()

    homeworks = Homework.objects.filter(user=request.user)
    # if the number of homework objects is 0 then it means they are completed
    if len(homeworks) == 0:
        homework_done = True
    # if the number of homeworks is 1 or more then they are incomplete
    else:
        homework_done = False
    context = {
        'homeworks':homeworks,
        'homework_done':homework_done,
        'form':form,
    }
    return render(request, 'homework.html', context)

@login_required
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    # if the status checkbox is ticked then changed then the assignment is completed
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')

@login_required
def delete_homework(request, pk):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')


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
    return redirect('todo')

def delete_todo(request, pk):
    todo.objects.get(id=pk).delete()
    return redirect('todo')


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





# YOUTUBE
@login_required
def youtube(request):
    if request.method == 'POST':
        form = YoutubeSearchForm(request.POST)
        # text is the field from YoutubeSearchForm
        text = request.POST['text']
        # VideosSearch is a module from youtube-search-python
        video = VideosSearch(text, limit=255)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime']
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context={
                'form':form,
                'results':result_list
            }
        return render(request, 'youtube.html', context)
    else:
        form = YoutubeSearchForm()
    context = {
        'form':form,
    }
    return render(request, 'youtube.html', context)
