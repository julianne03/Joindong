from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404

from account.models import Profile
from config import settings
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
    if request.user.profile.club:
        context = {'message': '이미 동아리에 가입되어 있습니다!'}
        return render(request, 'error_page.html', context)
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            club = form.save(commit=False)
            club.creator = request.user
            if 'main_poster' in request.FILES:
                club.main_poster = request.FILES['main_poster']
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
    context = {'club': club, 'members': members, 'user': request.user}
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
            if 'main_poster' in request.FILES:
                club.main_poster = request.FILES['main_poster']
            club.save()
            return redirect('jd:my_club', user_name=request.user.username)
    else:
        form = ClubForm(instance=club)
    context = {'form': form}
    return render(request, 'jd/create_club.html', context)


@login_required(login_url='account:login')
def update_club_message(request, club_title):
    club = get_object_or_404(Club, title=club_title)
    message, is_created = Message.objects.get_or_create(club=club)
    if request.user.profile.club != club or not request.user.profile.is_club_staff:
        context = {'message': '동아리 메세지 정보 수정권한이 없습니다!'}
        return render(request, 'error_page.html', context)
    if request.method == "POST":
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            message.save()
            return redirect('jd:my_club', user_name=request.user.username)
    else:
        form = MessageForm(instance=message)
    context = {'form': form}
    return render(request, 'jd/create_club_message.html', context)


@login_required(login_url='account:login')
def apply_club(request, club_title):
    club = get_object_or_404(Club, title=club_title)
    profile = Profile.objects.get(user=request.user)
    # club -> detail page club
    profile.club = club
    # is_club_staff -> False
    profile.save()
    return redirect('jd:club_detail', club_title=club.title)


@login_required(login_url='account:login')
def cancel_apply_club(request, club_title):
    print('cancel')
    club = get_object_or_404(Club, title=club_title)
    profile = Profile.objects.get(user=request.user)
    # club -> None or Null
    profile.club = None
    # is_club_staff -> False
    profile.save()
    return redirect('jd:club_detail', club_title=club.title)


@login_required(login_url='account:login')
def my_page(request, user_name):
    user = User.objects.get(username=user_name)
    context = {'user': user}
    return render(request, 'jd/my_page.html', context)


def delete_club(request, club_title):
    club = get_object_or_404(Club, title=club_title)
    if request.user != club.creator:
        return redirect('jd:my_club', club_title=club_title)
    club.delete()
    return redirect('jd:index')


@login_required(login_url='account:login')
def send_email(request, user_email):
    subject = "message"
    to = ["s2019w33@e-mirim.hs.kr"]
    from_email = settings.EMAIL_HOST_USER
    message = "sending email testing"
    EmailMessage(subject=subject, body=message, to=to,
                 from_email=from_email).send()
