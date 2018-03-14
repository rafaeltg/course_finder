from django.contrib import admin

from .models import Course, Location, Job

admin.site.register(Course)
admin.site.register(Location)
admin.site.register(Job)
