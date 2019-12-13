from rest_framework import serializers

from jalas_app import models
from jalas_app.models import Attendees, Option, Person, Poll



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


class PersonSerilizer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = ['email']


class AttendeesSerializer(serializers.Serializer):
    class Meta:
        model = models.Attendees
        fields = ('email')


class PollSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(allow_null=True)
    end_date = serializers.DateTimeField(allow_null=True)

    options_set = OptionSerializer(many=True)
    attendees = AttendeesSerializer(many=True)

    def create_options(self, options_set, poll):
        for option in options_set:
            option = Option.objects.create(**option)
            option.poll = poll
            option.save()

    def create_person(self, person_data, poll):
        print('I am here 6')
        for person in person_data:
            print('I am here 7: {}'.format(person))
            personn = Person.objects.create(**person) #TODO: create if not exists
            print('I am here 70: {}'.format(person))            
            attendee = Attendees.objects.create()
            print('I am here 700: {}'.format(person))
            attendee.person = personn
            print('I am here 7000: {}'.format(person))
            attendee.polls = poll
            attendee.save()

    def create(self, validated_data):
        print(validated_data)
        person_data = validated_data.pop('attendees')
        options_set = validated_data.pop('options_set')
        poll = Poll.objects.create(**validated_data)
        print('I am here 4')
        self.create_person(person_data, poll)
        print('I am here 5')

        self.create_options(options_set, poll)

        return poll

    class Meta:
        model = models.Poll
        fields = ('id', 'created', 'title', 'options_set', 'start_date', 'end_date', 'status', 'attendees')


