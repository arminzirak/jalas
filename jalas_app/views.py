import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view

from jalas_app.models import Meeting, Poll
from jalas_app.rooms_server import get_rooms, reserve_room
from jalas_app.serializers import MeetingSerializer

KHOSRAVI = 'rkhosravi'

class MeetingList(generics.ListAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer


class MeetingDetail(generics.RetrieveUpdateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer


@api_view(['GET'])
def get_rooms_available(request):
    start_date = request.query_params.get('start')
    end_date = request.query_params.get('end')
    rooms = get_rooms(start_date, end_date)
    return HttpResponse(json.dumps(rooms))


@api_view(['POST'])
def reserve_room(request):
	# print(request.body.get('id'))
	# print(data)
	data = json.loads(request.body.decode('utf-8'))
	id = data.get('id')
	room_number = data.get('room_number')
	print(id, room_number)
	poll = get_object_or_404(Poll, id = id)
	result = reserve_room(room_number, KHOSRAVI, poll.start_date, poll.end_date)
	# result = reserve_room(801, "rkhosravi", "2019-09-13T19:00:00", "2019-09-13T20:00:00")
	# result = "sf"
	print(result)
	return HttpResponse(result)
