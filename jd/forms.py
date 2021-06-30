from django import forms
from jd.models import Club, Message


class ClubForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ClubForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    deadline = forms.DateTimeField(
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'style': 'background-color: rgb(239,242,243); border: none'
            },
            format='%Y-%m-%dT%H:%M')
    )

    class Meta:
        model = Club
        fields = ['title', 'creator', 'main_poster', 'description', 'activities', 'good_things', 'etc_things', 'deadline', 'head_num']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['plan_message', 'pass_message', 'non_pass_message', 'send_date']
