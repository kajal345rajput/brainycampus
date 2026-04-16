from django.shortcuts import render  # only import render

def home(request):
    return render(request, 'home.html')  # request is automatically passed by Django