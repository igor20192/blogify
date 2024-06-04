from sys import argv
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and isinstance(instance, User):
        user = User.objects.filter(id=instance.id)
        if not Profile.objects.filter(user_id=instance.id) and user:
            Profile.objects.create(user=user[0])
