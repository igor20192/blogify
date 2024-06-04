from sys import argv
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Creates a user profile when a new user is created.

    Parameters:
    - sender: The model class that initiates the signal.
    - instance: Instance of the object on which the operation is performed.
    - created: Flag indicating whether the object was created.
    - **kwargs: Additional arguments.

    Actions:
    - When creating a new user, creates a user profile if it has not already been created.
    """
    if created and isinstance(instance, User) and "test" not in argv:
        user = User.objects.filter(id=instance.id)
        if not Profile.objects.filter(user_id=instance.id) and user:
            Profile.objects.create(user=user[0])
