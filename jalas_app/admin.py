from django.contrib import admin
from jalas_app.models import Meeting, Option, Poll, Vote, Person
# Register your models here.
admin.site.register(Meeting)
admin.site.register(Poll)
admin.site.register(Option)
admin.site.register(Vote)
admin.site.register(Person)