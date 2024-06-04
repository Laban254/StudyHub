from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('studyApp/', include('studyApp.urls', namespace='studyApp')), 
    path('home', TemplateView.as_view(template_name='dashboard.html'), name='home'),
    path('', TemplateView.as_view(template_name='about.html'), name='about'),
   
    
]