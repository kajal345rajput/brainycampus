from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # connect your app
    path('', include('myapp.urls')),
]