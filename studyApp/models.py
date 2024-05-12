from django.db import models

# A simple django user
from django.contrib.auth.models import User
from django_quill.fields import QuillField

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

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Todo"
        # The model will have this name in the admin page
        verbose_name_plural = "Todos"

class SharedNote(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(User, related_name='shared_notes')
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_by')
    shared_date = models.DateTimeField(auto_now_add=True)