from rest_framework import serializers

from jalas_app import models


class MeetingSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(allow_null=True)
    end_date = serializers.DateTimeField(allow_null=True)

    class Meta:
        model = models.Meeting
        fields = ['created', 'title', 'polls', 'start_date', 'end_date']
        depth = 1


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Poll
        fields = ['votes', 'meeting', 'start_date', 'end_date']
