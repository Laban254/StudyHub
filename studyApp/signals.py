# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from actstream import action
from .models import Note, FavoriteNote
from actstream.registry import register  # Import register from actstream.registry

# Register the Note model with actstream.registry
register(Note)


@receiver(post_save, sender=Note)
def track_note_creation(sender, instance, created, **kwargs):
    if created:
        action.send(instance.user, verb='created', action_object=instance,
                    description=f'Created note: "{instance.title}"')

@receiver(post_delete, sender=Note)
def track_note_deletion(sender, instance, **kwargs):
    action.send(instance.user, verb='deleted', action_object=instance,
                description=f'Deleted note: "{instance.title}"')

@receiver(post_save, sender=Note)
def track_note_update(sender, instance, created, **kwargs):
    if not created:
        action.send(instance.user, verb='updated', action_object=instance,
                    description=f'Updated note: "{instance.title}"')

@receiver(post_save, sender=Note)
def track_note_reminder(sender, instance, created, **kwargs):
    if instance.reminder:
        action.send(instance.user, verb='reminder_added', action_object=instance,
                    description=f'Reminder added for note: "{instance.title}"')

@receiver(post_save, sender=FavoriteNote)
def track_favorite_note(sender, instance, created, **kwargs):
    if created:
        action.send(instance.user, verb='added_to_favorites', action_object=instance.note,
                    description=f'Added note "{instance.note.title}" to favorites')


