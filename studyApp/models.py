from django.db import models

# A simple django user
from django.contrib.auth.models import User

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Notes"
        # The model will have this name in the admin page
        verbose_name_plural = "Notes"
