from django.urls import path
from . import views

from .views import (
    login_view,
    home_view,
    logout_view,

    # NOTES
    notes_view,
    add_note,
    delete_note,

    # TODO
    todo_list,
    add_todo,
    complete_todo,
    delete_todo,

    # ASSIGNMENT
    assignment_home,
    delete_assignment,
    complete_assignment,

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

    # ================= TODO =================
    path(
        'todo/',
        todo_list,
        name='todo'
    ),

    path(
        'todo/add/',
        add_todo,
        name='add_todo'
    ),

    path(
        'todo/complete/<int:pk>/',
        complete_todo,
        name='complete_todo'
    ),

    path(
        'todo/delete/<int:pk>/',
        delete_todo,
        name='delete_todo'
    ),

    # ================= ASSIGNMENT =================
    path(
        'assignments/',
        assignment_home,
        name='assignment_home'
    ),

    path(
        'delete-assignment/<int:id>/',
        delete_assignment,
        name='delete_assignment'
    ),

    path(
        'complete-assignment/<int:id>/',
        complete_assignment,
        name='complete_assignment'
    ),

    # ================== TIMETABLE ====================
    
    path('timetable/', views.timetable_view, name='timetable'),
    path('timetable/add/', views.add_timetable, name='add_timetable'),
    path('timetable/delete/<int:id>/', views.delete_timetable, name='delete_timetable'),
    path('timetable/edit/<int:id>/', views.edit_timetable, name='edit_timetable'),

]