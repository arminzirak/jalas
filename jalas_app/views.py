import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import api_view

from jalas_app import models
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
    poll_id = data.get('poll_id')
    print(poll_id)
    room_number = data.get('room_number')
    print(room_number)
    poll = get_object_or_404(Poll, id=poll_id)
    meeting = Meeting.objects.get(id=poll.meeting.id)
    start_date = str(poll.start_date).replace(" ", "T")[:-6]
    end_date = str(poll.end_date).replace(" ", "T")[:-6]
    print(start_date + ' ' + end_date)
    result, status_code = room_srever_reserver_room(room_number, KHOSRAVI, start_date, end_date)

    if status_code == 200:
        notify_meeting_owner("jalas.445317@gmail.com")
        meeting.status = models.MeetingStatus.finalized.value
    elif status_code == 400:
        pass
    else:
        status_code = 200
        meeting.status = models.MeetingStatus.pending.value
    meeting.save()
    return HttpResponse(result, status=status_code)
