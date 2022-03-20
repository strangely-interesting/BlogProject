from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.contrib.auth.models import User
from User.models import Profile, UnreadPost
from Blog.models import Post
from django.dispatch import receiver
from django.utils import timezone

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
    instance.profile.save()

@receiver(user_logged_out)
def update_last_visited(sender,request,user,**kwargs):
    user.profile.last_visited = timezone.now()
    user.profile.save()

@receiver(user_logged_in)
def set_unread_count(sender,request,user,**kwargs):
    for post in Post.objects.filter(post_date__gte=user.profile.last_visited):
        UnreadPost.objects.create(user=user,post=post)