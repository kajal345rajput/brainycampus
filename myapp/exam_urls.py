from django.urls import path
from . import views

urlpatterns = [

    path('', views.exam_list, name='exam_list'),

    path('create/', views.exam_create, name='exam_create'),

    path('edit/<int:pk>/', views.exam_edit, name='exam_edit'),

    path('delete/<int:pk>/', views.exam_delete, name='exam_delete'),
]