from django.db import models


# Create your models here.

class Meeting(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)

    class Meta:
        ordering = ['created']


class Poll(models.Model):
    meeting = models.ForeignKey(Meeting, related_name='polls', on_delete=models.CASCADE, null=True)
    votes_agree = models.IntegerField(default=0)
    votes_disagree = models.IntegerField(default=0)