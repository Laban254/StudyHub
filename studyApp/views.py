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
        return render(request, 'masomoyangu/books.html',  context)
    else:
        form = BookSearchForm()
    context = {
        'form':form,
    }
    return render(request, 'masomoyangu/books.html',  context)

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
        return render(request, 'masomoyangu/dictionary.html', context)
    else:
        form = DictionarySearchForm() 
        context = {
            'form':form,
        }
    return render(request, 'masomoyangu/dictionary.html', context)

# WIKI
@login_required
def wiki(request):
    form = WikiSearchForm()
    if request.method =='POST':
         # text is the field from DictionarySearchForm where user writes the book they want to search
        text = request.POST['text']
        form = WikiSearchForm(request.POST)
        # search variable reps the wikipedia page our text looks into
        search = wikipedia.page(text)
        context = {
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request, 'masomoyangu/wiki.html', context)
    else:
        form = WikiSearchForm()
        context = {
            'form':form
        }
    return render(request, 'masomoyangu/wiki.html', context)

# CONVERSION
@login_required
def conversion(request):
    if request.method == 'POST':
        # Form to choose either Length or Mass
        form = ConversionForm(request.POST)
        # when the measurement field choice is length
        if request.POST['measurement'] == 'length':
            # name of form
            measurement_form = ConversionLengthForm()
            context = {
                'form':form,
                'measurement_form':measurement_form,
                'input':True
            }
            # if there is a number inputed in the form
            if 'input' in request.POST:
                input = request.POST['input']
                first = request.POST['measure1']
                second = request.POST['measure2']
                # answer is an empty string at first
                answer = ''
                # if an integer input has been entered and is greater than 0
                if input and int(input) >= 0:
                    if first =='yard' and second == 'foot':
                        answer = f"{input} yard = {int(input)*3} foot"
                    if first == 'foot' and second == 'yard':
                        answer = f"{input} foot = {int(input)/3} yard"
                context ={
                    'form':form,
                    'measurement_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
        # when the measurement field choice is mass
        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {
                'form':form,
                'measurement_form':measurement_form,
                'input':True
            }
            # if a  number is entered in the form
            if 'input' in request.POST:
                input = request.POST['input']
                first = request.POST['measure1']
                second = request.POST['measure2']
                answer = ''
                if input and int(input) >= 0:
                    if first =='pound' and second == 'kilogram':
                        answer = f"{input} pound = {int(input)*0.453592} kilograms"
                    if first == 'kilogram' and second == 'pound':
                        answer = f"{input} kilogram = {int(input)*2.2062} pound"
                context ={
                    'form':form,
                    'measurement_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
    else:            
        form = ConversionForm()
        context = {
            'form':form,
            # initially input is set to false
            'input':False
        }
    return render(request, 'masomoyangu/conversion.html', context)