from django.urls import path
from . import views

urlpatterns = [

    # HOME
    path('', views.home, name='home'),

    # AUTH
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # NOTES
    path('notes/', views.notes, name='notes'),
    path('delete-note/<int:note_id>/', views.delete_note, name='delete_note'),

    # MODULES
    path('timetable/', views.timetable, name='timetable'),
    path('attendance/', views.attendance, name='attendance'),
    path('assignments/', views.assignments, name='assignments'),
    path('notebook/', views.notebook, name='notebook'),
    path('exam-planner/', views.exam_planner, name='exam_planner'),
    path('study-tracker/', views.study_tracker, name='study_tracker'),
    path('todo/', views.todo, name='todo'),
    path('grades/', views.grades, name='grades'),
    path('library/', views.library, name='library'),
    path('events/', views.events, name='events'),
    path('reminders/', views.reminders, name='reminders'),
]