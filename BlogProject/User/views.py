from django.shortcuts import render, redirect, get_object_or_404
from User.forms import UserRegistrationForm, ProfileUpdateForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account successfully created for {username} !')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    context = {'form':form}
    return render(request,'User/register_user.html',context=context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    profile_details = request.user.profile.get_profile_details()
    return render(request,'User/profile.html',
                  context={'profile': profile_details, 'u_form': u_form, 'p_form':p_form})

@login_required
def profile_others(request, username):
    user = get_object_or_404(User,username=username)
    profile_details = user.profile.get_profile_details()
    return render(request, 'User/profile.html', context={'profile': profile_details})