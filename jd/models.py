from django.db import models


class Club(models.Model):
    title = models.CharField(max_length=30)
    main_poster = models.ImageField(upload_to='main_poster')
    description = models.TextField(max_length=100)
    activities = models.TextField()
    good_things = models.TextField()
    etc_things = models.TextField(blank=True)
    deadline = models.DateTimeField()
    head_num = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = 'Clubs'

    def __str__(self):  # admin 사이트에서 보여지는 항목 이름
        return self.title


class Message(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    plan_message = models.TextField()
    pass_message = models.TextField()
    non_pass_message = models.TextField()
    send_date = models.DateTimeField()

    def __str__(self):
        return f'{self.club} message'

