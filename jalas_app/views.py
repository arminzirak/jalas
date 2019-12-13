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
from jalas_app.models import Meeting, Option, Poll, PollStatus
from jalas_app.notification_service import notify_Poll_owner
from jalas_app.rooms_server import get_rooms
from jalas_app.rooms_server import reserve_room as server_reserve_room
from jalas_app.serializers import MeetingSerializer, PollSerializer

class MeetingList(generics.ListAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer


class MeetingDetail(generics.RetrieveUpdateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

class PollList(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class PollDetail(generics.RetrieveUpdateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


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
    option_id = data.get('option_id')
    room_number = data.get('room_number')
    option = get_object_or_404(Option, id=option_id)
    poll = Poll.objects.get(id=option.Poll.id)
    start_date = str(option.start_date).replace(" ", "T")[:-6]
    end_date = str(option.end_date).replace(" ", "T")[:-6]
    result, status_code = reserve_room_service(poll, room_number, start_date, end_date)
    if status_code != 400:
        status_code = 200

    end_time = datetime.datetime.now()
    with open(TIMING_LOG_ADDRESS, "a") as f:
        f.write("Poll_processed,{},{},{},{}\n".format(poll.id, start_date, end_date, (end_time - start_time).microseconds))
    return HttpResponse(result, status=status_code)


@api_view(['POST'])
def cancel_Poll(request):
    data = json.loads(request.body.decode('utf-8'))
    poll_id = data.get('Poll_id')
    poll = get_object_or_404(poll, id=poll_id)
    poll.status = PollStatus.canceled
    poll.save()
    return HttpResponse(status=200)


@api_view(['POST'])
def finalize_Poll(request):
    start_time = datetime.datetime.now()
    data = json.loads(request.body.decode('utf-8'))
    option_id = data.get('option_id')
    room_number = data.get('room_number')
    option = get_object_or_404(Option, id=option_id)
    poll = Poll.objects.get(id=option.poll.id)
    
    start_date = str(Option.start_date).replace(" ", "T")[:-6]
    end_date = str(Option.end_date).replace(" ", "T")[:-6]
    result, status_code = reserve_room_service(poll, room_number, start_date, end_date)
    if status_code != 400:
        status_code = 200
        poll.status = PollStatus.finalized
        poll.save()
        meeting = Meeting(title = poll.title, start_date = poll.start_date, end_date = poll.end_date, room = poll.room)
        meeting.save()

    end_time = datetime.datetime.now()
    with open(TIMING_LOG_ADDRESS, "a") as f:
        f.write("poll_processed,{},{},{},{}\n".format(poll.id, start_date, end_date, (end_time - start_time).microseconds))



    return HttpResponse(status=200)


def reserve_retry(Poll, room_number, start_date, end_date):
    print('started retrying...')
    for i in range(3):
        print('attempt :{}'.format(i))
        result, status_code = reserve_room_service(Poll, room_number, start_date, end_date, attempt=i + 1)
        if status_code == 200:
            return


def reserve_room_service(Poll, room_number, start_date, end_date, attempt=1):
    result, status_code = server_reserve_room(room_number, USERNAME, start_date, end_date)
    if status_code == 200:
        with open(Poll_LOG_ADDRESS, "a") as f:
            f.write("Poll_finalized,{},{}\n".format(Poll.id, 'ok'))
        print('reserved in {} attempt'.format(i + 1))
        notify_Poll_owner(USER_GMAIL)
        Poll.status = models.PollStatus.finalized.value
        Poll.save()
        return result, status_code
    elif status_code == 400:
        with open(Poll_LOG_ADDRESS, "a") as f:
            f.write("Poll_cancelled,{},{}\n".format(Poll.id, 'room_already_reserved'))
        print('found room already reserved in {} attempt'.format(attempt))
        Poll.status = models.PollStatus.errored.value
        Poll.save()
        return result, status_code
    else:
        if attempt >= 4:
            with open(Poll_LOG_ADDRESS, "a") as f:
                f.write("Poll_cancelled,{},{}\n".format(Poll.id, 'sever_unavailable'))
            print('attempts ended up failed')
            Poll.status = models.PollStatus.errored.value
            Poll.save()
            return result, status_code
        elif attempt > 1:
            reserve_room_service(Poll, room_number, start_date, end_date, attempt + 1)
            Poll.status = models.PollStatus.pending.value
            Poll.save()
            return result, status_code
        else:
            threading.Thread(target=reserve_room_service, args=(Poll, room_number, start_date, end_date, 2)).start()
            result = "{\"message\": \"reservation is pending\"}"
            Poll.status = models.PollStatus.pending.value
            Poll.save()
            return result, status_code
