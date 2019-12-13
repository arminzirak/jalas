from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from jalas_app import views

urlpatterns = [
    path('Poll/', views.PollList.as_view()),
    path('Poll/<int:pk>', views.PollDetail.as_view()),
    path('room/available', views.get_rooms_available),
    path('room/reserve', views.reserve_room),
    path('room/cancel_Poll', views.cancel_Poll)
]
urlpatterns = format_suffix_patterns(urlpatterns)
