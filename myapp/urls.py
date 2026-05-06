from django.urls import path
from . import views

# core routes
urlpatterns = [
    path('', views.home, name='home'),

    # auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # notes
    path('notes/', views.notes, name='notes'),
    path('notes/delete/<int:note_id>/', views.delete_note, name='delete_note'),

    # attendance
    path('attendance/', views.attendance, name='attendance'),
    path('attendance/mark/<int:id>/<str:status>/', views.mark_attendance, name='mark_attendance'),

    # academic modules
    path('timetable/', views.timetable, name='timetable'),
    path('assignments/', views.assignments, name='assignments'),
    path('grades/', views.grades, name='grades'),

    # ❌ MISSING BEFORE → NOW FIXED
    path('exam-planner/', views.exam_planner, name='exam_planner'),

    # study tools
    path('notebook/', views.notebook, name='notebook'),
    path('study-tracker/', views.study_tracker, name='study_tracker'),
    path('todo/', views.todo, name='todo'),

    # library
    path('library/', views.library, name='library'),

    # events
    path('events/', views.events, name='events'),
    path('reminders/', views.reminders, name='reminders'),
]