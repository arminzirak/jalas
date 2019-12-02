from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from jalas_app import views

urlpatterns = [
    path('meeting/', views.MeetingList.as_view()),
    path('room/available', views.get_rooms_available)
]
urlpatterns = format_suffix_patterns(urlpatterns)
