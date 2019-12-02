from jalas_app.models import Meeting
from jalas_app.serializers import MeetingSerializer, PollSerializer
from rest_framework import generics


class MeetingList(generics.ListAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
