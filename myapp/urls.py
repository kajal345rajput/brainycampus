from django.urls import path
from .views import login_view, home_view, logout_view

urlpatterns = [
    path('', login_view, name='login'),          # local works
    path('login/', login_view, name='login'),    #  FIX for Render

    path('home/', home_view, name='home'),
    path('logout/', logout_view, name='logout'),
]