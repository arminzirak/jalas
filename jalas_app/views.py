import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import api_view

from jalas_app.models import Meeting, Poll
from jalas_app.notification_service import notify_meeting_owner
from jalas_app.rooms_server import get_rooms
from jalas_app.rooms_server import reserve_room as room_srever_reserver_room
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


@csrf_exempt
@api_view(['POST'])
def reserve_room(request):
    # print(request.body.get('id'))
    # print(data)
    data = json.loads(request.body.decode('utf-8'))
    id = data.get('poll_id')
    room_number = data.get('room_number')
    print(id, room_number)
    poll = get_object_or_404(Poll, id=id)
    start_date = str(poll.start_date).replace(" ", "T")[:-6]
    end_date = str(poll.start_date).replace(" ", "T")[:-6]
    result = room_srever_reserver_room(room_number, KHOSRAVI, start_date, end_date)

    notify_meeting_owner("jalas.445317@gmail.com")
    return HttpResponse(result)
