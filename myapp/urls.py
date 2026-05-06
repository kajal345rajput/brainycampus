from django.urls import path
from .views import login_view, home_view, logout_view

urlpatterns = [
    path('', login_view, name='login'),        # http://127.0.0.1:8000/
    path('home/', home_view, name='home'),     # dashboard after login
    path('logout/', logout_view, name='logout'),
]