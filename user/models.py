from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from news.models import Plans
from django.db.models.signals import post_save # Produce a signal if there is any database action.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE )
    subscribe =models.ForeignKey(Plans, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email 

# When any User instance created, Profile object instance is created automatically linked by User 
# @receiver(post_save, sender = User)
# def user_is_created(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user= instance)
#     else:
#         instance.profile.save()