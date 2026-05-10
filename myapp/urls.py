from django.urls import path, include
from . import views

urlpatterns = [

    # ================= AUTH =================
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),

    # ================= ATTENDANCE =================
    path('attendance/', views.attendance_view, name='attendance'),

    # ================= NOTES =================
    path('notes/', views.notes_view, name='notes'),
    path('add-note/', views.add_note, name='add_note'),
    path('delete-note/<int:id>/', views.delete_note, name='delete_note'),

    # ================= ASSIGNMENT =================
    path('assignments/', views.assignment_view, name='assignment'),
    path('submit-assignment/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
    path('view-submissions/<int:assignment_id>/', views.view_submissions, name='view_submissions'),
    path('delete-assignment/<int:assignment_id>/', views.delete_assignment, name='delete_assignment'),

    # ================= TIMETABLE =================
    path('timetable/', views.timetable_view, name='timetable'),
    path('timetable/add/', views.add_timetable, name='add_timetable'),
    path('timetable/delete/<int:id>/', views.delete_timetable, name='delete_timetable'),
    path('timetable/edit/<int:id>/', views.edit_timetable, name='edit_timetable'),
    path('add-student/', views.add_student, name='add_student'),

    # ================= EXAM PLANNER =================
    path('exams/', include('myapp.exam_urls')),

    #=======================Notebook====================#
    path('notebook/', views.notebook_view, name='notebook'),
    path('notebook/upload/', views.upload_material, name='upload_material'),
    path('delete-material/<int:pk>/', views.delete_material, name='delete_material'),

    #============= ADD STUDENT==============#
    path('students/add/', views.add_student, name='add_student'),
    path('students/', views.view_students, name='view_students'),
    path('students/edit/<int:pk>/', views.edit_student, name='edit_student'),
    path('students/delete/<int:pk>/', views.delete_student, name='delete_student'),

    #==================EVENTS================#
    path('events/', views.event_list, name='event_list'),
    path('events/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('events/add/', views.add_event, name='add_event'),
]