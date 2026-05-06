from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Note, Attendance


# auth
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

        return render(request, 'login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# home
@login_required
def home(request):
    return render(request, 'home.html')


# notes
@login_required
def notes(request):
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

    notes = Note.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'notes.html', {
        'notes': notes
    })


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.delete()
    return redirect('notes')


# attendance
@login_required
def attendance(request):
    if request.method == "POST":
        subject = request.POST.get('subject')

        if subject:
            Attendance.objects.get_or_create(
                user=request.user,
                subject=subject.strip().title()
            )

        return redirect('attendance')

    records = Attendance.objects.filter(user=request.user)

    total_subjects = records.count()

    avg_attendance = 0
    if total_subjects > 0:
        avg_attendance = round(
            sum(r.percentage() for r in records) / total_subjects,
            2
        )

    return render(request, 'attendance.html', {
        'records': records,
        'total_subjects': total_subjects,
        'avg_attendance': avg_attendance
    })


# FIXED: mark attendance (THIS WAS MISSING)
@login_required
def mark_attendance(request, id, status):
    record = get_object_or_404(Attendance, id=id, user=request.user)

    if status == "present":
        record.attended_classes += 1
        record.total_classes += 1

    elif status == "absent":
        record.total_classes += 1

    record.save()

    return redirect('attendance')


# academic modules
@login_required
def timetable(request):
    return render(request, 'timetable.html')


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