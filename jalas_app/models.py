import datetime

from django.db import models


# Create your models here.

class Meeting(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)

    start_date = models.DateTimeField(default=datetime.datetime.now())
    end_date = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        ordering = ['created']


class Poll(models.Model):
    meeting = models.ForeignKey(Meeting, related_name='polls', on_delete=models.CASCADE, null=True)
    votes_agree = models.IntegerField(default=0)
    votes_disagree = models.IntegerField(default=0)

    # TODO: use HoldTime
    start_date = models.DateTimeField(default=datetime.datetime.now())
    end_date = models.DateTimeField(default=datetime.datetime.now())


class HoldTime(object):
    def ___init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return self.start_date + '|' + self.end_date
