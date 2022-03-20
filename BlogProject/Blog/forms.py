from django import forms
from django.forms.models import inlineformset_factory
from Blog.models import Post, PostImage

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author','post_date')

PostImageFormSet = inlineformset_factory(Post,PostImage,fields=['image'],can_delete=True,extra=0)