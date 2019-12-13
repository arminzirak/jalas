from rest_framework import serializers

from jalas_app import models



class MeetingSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(allow_null=True)
    end_date = serializers.DateTimeField(allow_null=True)

    class Meta:
        model = models.Meeting
        fields = ['id', 'created', 'title', 'start_date', 'end_date']
        depth = 1


class PollSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(allow_null=True)
    end_date = serializers.DateTimeField(allow_null=True)

    class Meta:
        model = models.Poll
        fields = ['id', 'created', 'title', 'Options', 'start_date', 'end_date', 'status']
        depth = 1




class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Option
        fields = ['id', 'votes', 'Poll', 'start_date', 'end_date']
