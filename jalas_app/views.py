import json
import threading

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
    return HttpResponse(json.dumps(str(rooms)))


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
    print('result: ' + str(result))
    print('status_code: ' + str(status_code))
    if status_code == 200:
        notify_meeting_owner("jalas.445317@gmail.com")
        meeting.status = models.MeetingStatus.finalized.value
        with open("meetings_log.csv", "a") as f:
            f.write("meeting_finalized,{},{}\n".format(meeting.id, 'ok'))
    elif status_code == 400:
        with open("meetings_log.csv", "a") as f:
            f.write("meeting_cancelled,{},{}\n".format(meeting.id, 'room_already_reserved'))
        pass
    else:
        status_code = 200
        meeting.status = models.MeetingStatus.pending.value
        threading.Thread(target=reserve_retry(meeting, room_number, start_date, end_date)).start()
        result = "{\"message\": \"reservation is pending\"}"
    meeting.save()
    return HttpResponse(result, status=status_code)


@api_view(['POST'])
def cancel_meeting(request):
    data = json.loads(request.body.decode('utf-8'))
    meeting_id = data.get('meeting_id')
    meeting = get_object_or_404(Meeting, id=meeting_id)
    meeting.status = 3
    meeting.save()
    return HttpResponse(status=200)


def reserve_retry(meeting, room_number, start_date, end_date):
    print('started retrying...')
    for i in range(3):
        print('attempt {}'.format(i + 1))
        result, status_code = room_srever_reserver_room(room_number, KHOSRAVI, start_date, end_date)
        if status_code == 200:
            with open("meetings_log.csv", "a") as f:
                f.write("meeting_finalized,{},{}\n".format(meeting.id, 'ok'))
            print('reserved in {} attempt'.format(i + 1))
            notify_meeting_owner("jalas.445317@gmail.com")
            meeting.status = models.MeetingStatus.finalized.value
            return
        elif status_code == 400:
            with open("meetings_log.csv", "a") as f:
                f.write("meeting_cancelled,{},{}\n".format(meeting.id, 'room_already_reserved'))
            print('found room already reserved in {} attempt'.format(i + 1))
            meeting.status = models.MeetingStatus.errored.value
            return
    with open("meetings_log.csv", "a") as f:
        f.write("meeting_cancelled,{},{}\n".format(meeting.id, 'sever_unavailable'))
    print('attempts ended up failed')
    meeting.status = models.MeetingStatus.errored.value
