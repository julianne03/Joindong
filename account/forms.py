from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from account.models import Profile


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['st_num', 'nickname', 'image', 'phone_num']


class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['email', 'username']
