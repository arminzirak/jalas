from django.db import models


# Create your models here.

class Meeting(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)

    class Meta:
        ordering = ['created']


class Poll(models.Model):
    votes = models.IntegerField(default=0)