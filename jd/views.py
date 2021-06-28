from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from account.models import Profile
from jd.forms import ClubForm, MessageForm
from jd.models import Club, Message


@login_required(login_url='account:login')
def index(request):
    return render(request, 'jd/index.html')


@login_required(login_url='account:login')
def club_list(request):
    clubs = Club.objects.order_by('deadline')
    context = {'list': clubs}
    return render(request, 'jd/club_list.html', context)


@login_required(login_url='account:login')
def create_club(request):
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            club = form.save(commit=False)
            club.creator = request.user
            club.main_poster = request.FILES['main_poster_image']
            club.save()
            profile = Profile.objects.get(user=request.user)
            profile.club = club
            profile.is_club_staff = True
            profile.save()
        return redirect('jd:club_detail', club_title=club.title)
    else:
        form = ClubForm()
    return render(request, 'jd/create_club.html', {'form': form})


@login_required(login_url='account:login')
def detail_club(request, club_title):
    club = Club.objects.get(title=club_title)
    members = User.objects.filter(profile__club=club, profile__is_club_staff=True)
    context = {'club': club, 'members': members}
    return render(request, 'jd/club_detail.html', context)


# 자기 자신만 들어갈 수 있도록 만들기
@login_required(login_url='account:login')
def my_club(request, user_name):
    user = User.objects.get(username=user_name)
    members = User.objects.filter(profile__club=user.profile.club, profile__is_club_staff=True)
    applicants = User.objects.filter(profile__club=user.profile.club, profile__is_club_staff=False)
    if request.user.username == user_name:
        if user.profile.club and user in members:
            context = {'user': user, 'club': user.profile.club, 'members': members, 'applicants': applicants}
            return render(request, 'jd/my_club.html', context)
        context = {'user': user, 'message': '현재 소속되어 있는 동아리가 없습니다'}
        return render(request, 'error_page.html', context)
    context = {'user': user, 'message': '다른 사람의 동아리 페이지에 접근하였습니다!'}
    return render(request, 'error_page.html', context)


@login_required(login_url='account:login')
def update_club(request, club_title):
    club = get_object_or_404(Club, title=club_title)
    if request.user.profile.club != club or not request.user.profile.is_club_staff:
        context = {'message': '동아리 정보 수정권한이 없습니다!'}
        return render(request, 'error_page.html', context)
    if request.method == "POST":
        form = ClubForm(request.POST, instance=club)
        if form.is_valid():
            club = form.save(commit=False)
            club.creator = request.user
            club.main_poster = request.FILES['main_poster_image']
            club.save()
            return redirect('jd:club_detail', club_title=club.title)
    else:
        form = ClubForm(instance=club)
    context = {'form': form}
    return render(request, 'jd/create_club.html', context)


def update_club_message(request, club_title):
    club = get_object_or_404(Club, title=club_title)
    message, is_created = Message.objects.get_or_create(club=club)
    if request.user.profile.club != club or not request.user.profile.is_club_staff:
        context = {'message': '동아리 메세지 정보 수정권한이 없습니다!'}
        return render(request, 'error_page.html', context)
    if request.method == "POST":
        if is_created:
            form = MessageForm(request.POST, instance=message)
        else:
            form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.save()
            return redirect('jd:my_club', club_title=club.title)
    else:
        if is_created:
            form = MessageForm(request.POST, instance=message)
        else:
            form = MessageForm(request.POST)
    context = {'form': form}
    return render(request, 'jd/create_club_message.html', context)
