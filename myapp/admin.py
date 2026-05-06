from django.contrib import admin
from .models import (
    Timetable, Attendance, Assignment, Note,
    Todo, StudyTracker, ExamPlanner,
    Grade, Library, Event, Reminder
)

admin.site.register(Timetable)
admin.site.register(Attendance)
admin.site.register(Assignment)
admin.site.register(Note)
admin.site.register(Todo)
admin.site.register(StudyTracker)
admin.site.register(ExamPlanner)
admin.site.register(Grade)
admin.site.register(Library)
admin.site.register(Event)
admin.site.register(Reminder)