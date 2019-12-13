import datetime
import enum

from django.db import models


class PollStatus(enum.Enum):
    init = 0
    pending = 1
    finalized = 2
    canceled = 3
    errored = 4


class Poll(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    room = models.IntegerField(null=True, blank=True)

    status = models.IntegerField(choices=((tag.value, tag.name) for tag in PollStatus), default=0)

    class Meta:
        ordering = ['created']


class Option(models.Model):
    poll = models.ForeignKey(Poll, related_name = 'options_set', on_delete=models.CASCADE, null=True)

    start_date = models.DateTimeField(default=datetime.datetime.now())
    end_date = models.DateTimeField(default=datetime.datetime.now())


class Vote(models.Model):
    vote = models.IntegerField(default = 0)
    option = models.ForeignKey(Option, related_name = 'votes_set', on_delete=models.CASCADE)


class Meeting(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    room = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['created']


class HoldTime(object):
    def ___init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return self.start_date + '|' + self.end_date


class Person(models.Model):
    email = models.CharField(max_length= 100)
    name = models.CharField(default = "Asgar", max_length = 100)

class Attendees(models.Model):
    person = models.ForeignKey(Person, related_name = 'attendees', on_delete=models.CASCADE, null=True, blank=True)
    polls = models.ForeignKey(Poll, related_name = 'attendees', on_delete=models.CASCADE, null=True, blank=True)
