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
