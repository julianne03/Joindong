from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    st_num = models.IntegerField()
    nickname = models.CharField(max_length=20)
    image = models.ImageField(blank=True, upload_to="%Y/%m/%d")
    phone_num = models.CharField(max_length=20)
    club_name = models.TextField(blank=True)
    is_club_staff = models.BooleanField(default=False)
