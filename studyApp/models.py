from django.db import models

# A simple django user
from django.contrib.auth.models import User
from django_quill.fields import QuillField
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = QuillField()
    # completed_at = models.DateTimeField(help_text="None if the note isn't completed. Contain datetime when the note was completed", blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reminder = models.DateTimeField(blank=True, null=True)
    favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Notes"
        # The model will have this name in the admin page
        verbose_name_plural = "Notes"


class FavoriteNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

class Todo(models.Model):
    pass

class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    description = QuillField()
    due = models.DateField()
    is_finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Homework"
        # The model will have this name in the admin page
        verbose_name_plural = "Homeworks"

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    completed = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    # tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

# Predefined categories for the study hub
CATEGORIES = [
    'Assignments',
    'Exams',
    'Lectures',
    'Research',
    'Study Sessions',
    'Extracurricular Activities',
    'Personal Development',
    'Group Projects',
    'Meetings',
    'Miscellaneous',
]

# Signal to populate categories after migration
@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    if sender.name == 'studyApp':
        for category_name in CATEGORIES:
            Category.objects.get_or_create(name=category_name)


class SharedNote(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(User, related_name='shared_notes')
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_by')
    shared_date = models.DateTimeField(auto_now_add=True)