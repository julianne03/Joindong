from django import forms
from jd.models import Club


class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['title', 'creator', 'description', 'activities', 'good_things', 'etc_things', 'deadline', 'head_num']