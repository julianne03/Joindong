from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from account.forms import UserForm, ProfileForm
from account.models import Profile


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('account:profile_signup')
    else:
        form = UserForm()
    return render(request, 'account/signup.html', {'form': form})


@login_required(login_url='account:login')
def profile_signup(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        form.user = request.user
        if form.is_valid():
            profile = form.save(commit=False)
            profile.image = request.FILES['profile_image']
            profile.save()
            return redirect('jd:index')
        return redirect('account:profile_signup')
    else:
        profile, is_created = Profile.objects.get_or_create(user=request.user)
        form = ProfileForm(instance=profile)
        return render(request, 'account/profile_signup.html', {'form': form, 'profile': profile})
