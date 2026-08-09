from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .models import Profile
from django.dispatch import receiver

'''  Django create the signal when the new user is created, it likes the Profile model with django build-in
user model to create the profile for each new user without need to add it manually.

"post_save" send the signal after save.
"@receiver" decorator receive the signal that send by the post_save. '''

@receiver(post_save, sender=User)
def create_profile(sender,instance,created,**kwargs):

    if created:
        Profile.objects.create(user=instance)

        