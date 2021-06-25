from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from account.models import Profile


class UserForm(UserCreationForm):
    st_num = forms.IntegerField(label="학번")
    email = forms.EmailField(label="이메일")
    nickname = forms.CharField(label="이름")
    image = forms.ImageField(label="프로필 이미지")
    phone_num = forms.CharField(label="핸드폰 번호")

    class Meta:
        model = User, Profile
        fields = ("username", "st_num", "email", "nickname", "image", "phone_num", "password1", "password2")
