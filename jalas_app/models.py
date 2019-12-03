import datetime
import enum

from django.db import models


class MeetingStatus(enum.Enum):
    init = 0
    pending = 1
    finalized = 2
    canceled = 3
    errored = 4


class Meeting(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    room = models.IntegerField(null=True, blank=True)

    status = models.IntegerField(choices=((tag.value, tag.name) for tag in MeetingStatus))

    class Meta:
        ordering = ['created']


class Poll(models.Model):
    meeting = models.ForeignKey(Meeting, related_name='polls', on_delete=models.CASCADE, null=True)
    votes_agree = models.IntegerField(default=0)
    votes_disagree = models.IntegerField(default=0)

    start_date = models.DateTimeField(default=datetime.datetime.now())
    end_date = models.DateTimeField(default=datetime.datetime.now())


class HoldTime(object):
    def ___init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return self.start_date + '|' + self.end_date

