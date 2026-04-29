from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),   # default page = login
    path('home/', views.home, name='home'),     # dashboard
    path('logout/', views.logout_view, name='logout'),
]