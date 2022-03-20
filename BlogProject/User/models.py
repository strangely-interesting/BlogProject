from django.db import models
from django.contrib.auth.models import User
from Blog.models import Post
from datetime import datetime

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_image = models.ImageField(default='default.jpg',upload_to='profile_images')
    about_me = models.TextField(max_length=500,blank=True,null=True)
    age = models.CharField(max_length=10,blank=True,null=True,default='Not provided')
    organization = models.CharField(max_length=100,blank=True,null=True,default='Not provided')
    city = models.CharField(max_length=100,blank=True,null=True,default='Not provided')
    insta_profile = models.CharField(max_length=200,blank=True,null=True,default='#')
    facebook_profile = models.CharField(max_length=200,blank=True,null=True,default='#')
    linkedin_profile = models.CharField(max_length=200,blank=True,null=True,default='#')
    twitter_profile = models.CharField(max_length=200,blank=True,null=True,default='#')
    last_visited = models.DateTimeField(null=True,default=datetime.now())

    def __str__(self):
        return f'Profile for {self.user.first_name} {self.user.last_name}'

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def get_profile_details(self):
        profile_details = {'username': self.user.username,
                           'full_name': self.user.first_name + ' ' + self.user.last_name,
                           'email': self.user.email,
                           'profile_image_url': self.profile_image.url,
                           'about_me':self.about_me,
                           'age': self.age,
                           'organization': self.organization,
                           'city': self.city,
                           'insta_profile': self.insta_profile,
                           'facebook_profile': self.facebook_profile,
                           'linkedin_profile': self.linkedin_profile,
                           'twitter_profile': self.twitter_profile
                           }
        return profile_details

class UnreadPost(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.OneToOneField(Post,on_delete=models.CASCADE)
