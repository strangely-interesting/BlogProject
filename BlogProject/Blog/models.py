from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    post_date = models.DateTimeField()
    post_caption = models.CharField(max_length=100, verbose_name='Caption for post')
    post_text = models.TextField(blank=True,null=True, verbose_name='Post text')

    def __str__(self):
        return self.post_caption

    def get_absolute_url(self):
        return reverse('Blog:post_details',kwargs={'pk': self.id})

class PostImage(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images',null=True)

class PostLike(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    liked_date_time = models.DateTimeField()

class PostComment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    comment_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    comment_date_time = models.DateTimeField()
    comment_text = models.CharField(max_length=2000)

    def __str__(self):
        return self.comment_text

