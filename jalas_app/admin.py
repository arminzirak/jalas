from django.contrib import admin
from jalas_app.models import Attendees, Meeting, Option, Person, Poll, Vote
# Register your models here.
admin.site.register(Meeting)
admin.site.register(Poll)
admin.site.register(Option)
admin.site.register(Vote)
admin.site.register(Person)
admin.site.register(Attendees)