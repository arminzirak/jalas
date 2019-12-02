from rest_framework import serializers

from jalas_app import models


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Meeting
        fields = ['created', 'title', 'polls']
        depth = 1


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Poll
        fields = ['votes']
