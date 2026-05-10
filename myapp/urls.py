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
]