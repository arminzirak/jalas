from django.http import HttpResponse
from rest_framework import generics
from rest_framework.decorators import api_view

from jalas_app.models import Meeting
from jalas_app.rooms_server import get_rooms
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
    return HttpResponse(rooms)
