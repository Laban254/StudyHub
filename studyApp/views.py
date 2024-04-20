from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import RegistrationForm

from django.shortcuts import render
from django.views import View

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