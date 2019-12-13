from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from jalas_app import views

urlpatterns = [
    path('Poll/', views.PollList.as_view()),
    path('Poll/<int:pk>', views.PollDetail.as_view()),
    path('Poll/<int:pk>/finalize', views.finalize_Poll),
    path('room/available', views.get_rooms_available),
    path('room/reserve', views.reserve_room), #TODO: should be removed
    path('room/cancel_Poll', views.cancel_Poll),
    path('meeting/', views.MeetingList.as_view()),
    path('meeting/<int:pk>', views.MeetingDetail.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)
