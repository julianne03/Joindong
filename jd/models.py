from django.db import models


class Club(models.Model):
    title = models.CharField(max_length=30)
    main_poster = models.ImageField()
    description = models.TextField(max_length=100)
    activities = models.TextField()
    good_things = models.TextField()
    etc_things = models.TextField()
    deadline = models.DateTimeField()
    head_num = models.IntegerField(default=1)


class Message(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    plan_message = models.TextField()
    pass_message = models.TextField()
    non_pass_message = models.TextField()

