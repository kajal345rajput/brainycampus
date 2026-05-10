from django.contrib import admin
from .models import (
    Timetable, Attendance, Assignment, Note, 
    Exam, Event
)

admin.site.register(Timetable)
admin.site.register(Attendance)
admin.site.register(Assignment)
admin.site.register(Note)
admin.site.register(Exam)    
admin.site.register(Event)
 
 
 