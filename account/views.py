from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from account.forms import UserForm, ProfileForm, CustomUserChangeForm, SearchForm
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
            messages.success(request, '프로필 정보를 입력해주세요!')
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
            if 'image' in request.FILES:
                form.user.profile.image = request.FILES['image']
            profile.save()
            messages.success(request, '회원가입이 성공적으로 완료되었습니다!')
            return redirect('jd:index')
        return redirect('account:profile_signup')
    else:
        profile, is_created = Profile.objects.get_or_create(user=request.user)
        form = ProfileForm(instance=profile)
        return render(request, 'account/profile_signup.html', {'form': form, 'profile': profile})


@login_required(login_url='account:login')
def update_user(request, user_name):
    if request.method == 'POST':
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_change_form.is_valid() and profile_form.is_valid():
            user_change_form.save()
            profile = profile_form.save(commit=False)
            if 'image' in request.FILES:
                profile.user.profile.image = request.FILES['image']
            profile.save()
            messages.success(request, '회원 정보가 정상적으로 수정되었습니다!')
            return redirect('jd:my_page', user_name=request.user.username)
        return redirect('account:update_user', user_name=request.user.username)
    else:
        user_change_form = CustomUserChangeForm(instance=request.user)
        profile, create = Profile.objects.get_or_create(user=request.user)
        profile_form = ProfileForm(instance=profile)
        context = {'user_change_form': user_change_form, 'profile_form': profile_form, 'profile': profile}
        return render(request, 'account/update_user.html', context)


@login_required(login_url='account:login')
def delete_user(request, user_name):
    user = get_object_or_404(User, username=user_name)
    if request.user != user:
        return redirect('jd:my_page', user_name=user_name)
    user.delete()
    messages.success(request, '정상적으로 회원 탈퇴가 완료되었습니다!')
    return redirect('jd:index')


@login_required(login_url='account:login')
def search_user(request):
    form = SearchForm(request.POST)
    if form.is_valid():
        username = request.GET.get('s_user_name')
        return redirect('jd:my_page', user_name=username)
    return render(request, 'jd/index.html')