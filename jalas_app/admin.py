from django.contrib import admin
from jalas_app.models import Poll, Option, Meeting
# Register your models here.
admin.site.register(Meeting)
admin.site.register(Poll)
admin.site.register(Option)

