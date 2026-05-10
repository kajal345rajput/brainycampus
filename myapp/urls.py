from django.urls import path, include
from . import views

from .views import (
    login_view,
    home_view,
    logout_view,

    # NOTES
    notes_view,
    add_note,
    delete_note,

    # ASSIGNMENT
    assignment_view,
    submit_assignment,
    view_submissions,
    delete_assignment,

    # ATTENDANCE
    attendance_view,
)

urlpatterns = [

     
    # ================= AUTH =================
    path('', login_view, name='login'),

    path('login/', login_view, name='login'),

    path('home/', home_view, name='home'),

    path('logout/', logout_view, name='logout'),

    # ================= ATTENDANCE =================
    path(
        'attendance/',
        attendance_view,
        name='attendance'
    ),

    # ================= NOTES =================
    path(
        'notes/',
        notes_view,
        name='notes'
    ),

    path(
        'add-note/',
        add_note,
        name='add_note'
    ),

    path(
        'delete-note/<int:id>/',
        delete_note,
        name='delete_note'
    ),

     # ================= ASSIGNMENT =================

path(
    'assignments/',
    views.assignment_view,
    name='assignment'
),

path(
    'submit-assignment/<int:assignment_id>/',
    views.submit_assignment,
    name='submit_assignment'
),

path(
    'view-submissions/<int:assignment_id>/',
    views.view_submissions,
    name='view_submissions'
),

path(
    'delete-assignment/<int:assignment_id>/',
    views.delete_assignment,
    name='delete_assignment'
),

    # ================== TIMETABLE ====================
    
    path('timetable/', views.timetable_view, name='timetable'),
    path('timetable/add/', views.add_timetable, name='add_timetable'),
    path('timetable/delete/<int:id>/', views.delete_timetable, name='delete_timetable'),
    path('timetable/edit/<int:id>/', views.edit_timetable, name='edit_timetable'),
    path('add-student/', views.add_student, name='add_student'),
   
   #==============EXAMPLANNER=======#
   path('', include('myapp.exam_urls')),
]