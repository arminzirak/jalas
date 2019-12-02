from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from jalas_app import views

urlpatterns = [
    path('meeting/', views.MeetingList.as_view()),
    path('meeting/<int:pk>', views.MeetingDetail.as_view()),
    path('room/available', views.get_rooms_available),
    path('room/reserve', views.reserve_room)
]
urlpatterns = format_suffix_patterns(urlpatterns)
