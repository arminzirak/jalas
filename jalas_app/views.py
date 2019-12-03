import datetime
import json
import threading

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import api_view

from jalas_app import models
from jalas_app.config import *
from jalas_app.models import Meeting, Poll
from jalas_app.notification_service import notify_meeting_owner
from jalas_app.rooms_server import get_rooms
from jalas_app.rooms_server import reserve_room as server_reserve_room
from jalas_app.serializers import MeetingSerializer


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
    start_time = datetime.datetime.now()
    data = json.loads(request.body.decode('utf-8'))
    poll_id = data.get('poll_id')
    room_number = data.get('room_number')
    poll = get_object_or_404(Poll, id=poll_id)
    meeting = Meeting.objects.get(id=poll.meeting.id)
    start_date = str(poll.start_date).replace(" ", "T")[:-6]
    end_date = str(poll.end_date).replace(" ", "T")[:-6]
    result, status_code = reserve_room_service(meeting, room_number, start_date, end_date)
    if status_code != 400:
        status_code = 200

    end_time = datetime.datetime.now()
    with open(TIMING_LOG_ADDRESS, "a") as f:
        f.write("meeting_processed,{},{},{},{}\n".format(meeting.id, start_date, end_date, (end_time - start_time).microseconds))
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
        print('attempt :{}'.format(i))
        result, status_code = reserve_room_service(meeting, room_number, start_date, end_date, attempt=i + 1)
        if status_code == 200:
            return


def reserve_room_service(meeting, room_number, start_date, end_date, attempt=1):
    result, status_code = server_reserve_room(room_number, USERNAME, start_date, end_date)
    if status_code == 200:
        with open(MEETING_LOG_ADDRESS, "a") as f:
            f.write("meeting_finalized,{},{}\n".format(meeting.id, 'ok'))
        print('reserved in {} attempt'.format(i + 1))
        notify_meeting_owner(USER_GMAIL)
        meeting.status = models.MeetingStatus.finalized.value
        meeting.save()
        return result, status_code
    elif status_code == 400:
        with open(MEETING_LOG_ADDRESS, "a") as f:
            f.write("meeting_cancelled,{},{}\n".format(meeting.id, 'room_already_reserved'))
        print('found room already reserved in {} attempt'.format(attempt))
        meeting.status = models.MeetingStatus.errored.value
        meeting.save()
        return result, status_code
    else:
        if attempt >= 4:
            with open(MEETING_LOG_ADDRESS, "a") as f:
                f.write("meeting_cancelled,{},{}\n".format(meeting.id, 'sever_unavailable'))
            print('attempts ended up failed')
            meeting.status = models.MeetingStatus.errored.value
            meeting.save()
            return result, status_code
        elif attempt > 1:
            reserve_room_service(meeting, room_number, start_date, end_date, attempt + 1)
            meeting.status = models.MeetingStatus.pending.value
            meeting.save()
            return result, status_code
        else:
            threading.Thread(target=reserve_room_service, args=(meeting, room_number, start_date, end_date, 2)).start()
            result = "{\"message\": \"reservation is pending\"}"
            meeting.status = models.MeetingStatus.pending.value
            meeting.save()
            return result, status_code
