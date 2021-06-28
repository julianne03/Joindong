from django import forms
from jd.models import Club, Message


class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['title', 'creator', 'description', 'activities', 'good_things', 'etc_things', 'deadline', 'head_num']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['plan_message', 'pass_message', 'non_pass_message', 'send_date']
