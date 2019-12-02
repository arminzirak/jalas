from django.urls import path

from jalas_app import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('meeting/', views.MeetingList.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
