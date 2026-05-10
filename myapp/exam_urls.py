from django.urls import path
from . import views

urlpatterns = [

    path('exams/', views.exam_list, name='exam_list'),

    path('exams/create/', views.exam_create, name='exam_create'),

    path('exams/edit/<int:pk>/', views.exam_edit, name='exam_edit'),

    path('exams/delete/<int:pk>/', views.exam_delete, name='exam_delete'),
]