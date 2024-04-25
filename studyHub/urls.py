from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('studyApp/', include('studyApp.urls', namespace='studyApp')), 
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
]