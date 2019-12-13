from rest_framework import serializers

from jalas_app import models



class MeetingSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(allow_null=True)
    end_date = serializers.DateTimeField(allow_null=True)

    class Meta:
        model = models.Meeting
        fields = ['id', 'created', 'title', 'start_date', 'end_date']
        depth = 1


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vote
        fields = ['id', 'vote']


class OptionSerializer(serializers.ModelSerializer):
    votes_set = VoteSerializer(read_only=True, many=True)
    class Meta:
        model = models.Option
        fields = ['id', 'votes_set', 'start_date', 'end_date']


class PollSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(allow_null=True)
    end_date = serializers.DateTimeField(allow_null=True)

    options_set = OptionSerializer(read_only=True, many=True)

    class Meta:
        model = models.Poll
        fields = ('id', 'created', 'title', 'options_set', 'start_date', 'end_date', 'status')



