from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from User.models import Profile

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password1','password2']

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id':'user_first_name'}))
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name','last_name','email']

class ProfileUpdateForm(forms.ModelForm):
    age = forms.CharField(required=False)
    organization = forms.CharField(required=False)
    city = forms.CharField(required=False)
    insta_profile = forms.CharField(required=False)
    facebook_profile = forms.CharField(required=False)
    linkedin_profile = forms.CharField(required=False)
    twitter_profile = forms.CharField(required=False)

    class Meta:
        model = Profile
        fields = ['about_me','age','organization','city','insta_profile','facebook_profile','linkedin_profile'
                  ,'twitter_profile','profile_image']
        success_url = '/profile/'