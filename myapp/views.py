from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Note


# ---------------- AUTH ---------------- #

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ---------------- HOME ---------------- #

@login_required
def home(request):
    return render(request, 'home.html')


# ---------------- NOTES (FULL CRUD PARTIAL) ---------------- #

@login_required
def notes(request):
    # ADD NOTE
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:
            Note.objects.create(
                user=request.user,
                title=title,
                content=content
            )
        return redirect('notes')

    # SHOW USER NOTES
    notes = Note.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'notes.html', {'notes': notes})


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.delete()
    return redirect('notes')


# ---------------- OTHER MODULES ---------------- #

@login_required
def timetable(request):
    return render(request, 'timetable.html')


@login_required
def attendance(request):
    return render(request, 'attendance.html')


@login_required
def assignments(request):
    return render(request, 'assignments.html')


@login_required
def notebook(request):
    return render(request, 'notebook.html')


@login_required
def exam_planner(request):
    return render(request, 'exam_planner.html')


@login_required
def study_tracker(request):
    return render(request, 'study_tracker.html')


@login_required
def todo(request):
    return render(request, 'todo.html')


@login_required
def grades(request):
    return render(request, 'grades.html')


@login_required
def library(request):
    return render(request, 'library.html')


@login_required
def events(request):
    return render(request, 'events.html')


@login_required
def reminders(request):
    return render(request, 'reminders.html')