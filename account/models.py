from django.contrib.auth.models import User
from django.db import models

from jd.models import Club


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    st_num = models.IntegerField(null=True)
    nickname = models.CharField(max_length=20)
    introduction = models.CharField(blank=True, max_length=100)
    image = models.ImageField(blank=True, upload_to="profile_image/")
    phone_num = models.CharField(max_length=20)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    is_club_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
