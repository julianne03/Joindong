from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    st_num = models.IntegerField(null=True)
    nickname = models.CharField(max_length=20)
    image = models.ImageField(blank=True, upload_to="profile_image/")
    phone_num = models.CharField(max_length=20)
    club_name = models.TextField(blank=True)
    is_club_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
