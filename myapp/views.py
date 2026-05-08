from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Attendance, Note, Todo, Assignment, Timetable


# ================= LOGIN =================
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )

        if user:
            login(request, user)
            return redirect('home')

        return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


# ================= HOME =================
@login_required(login_url='/login/')
def home_view(request):
    return render(request, 'home.html')


# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect('/login/')


# ================= ATTENDANCE =================
@login_required
def attendance_view(request):

    if request.user.is_staff:

        students = User.objects.filter(is_staff=False)

        if request.method == "POST":
            student = get_object_or_404(User, id=request.POST.get('student'))

            Attendance.objects.update_or_create(
                student=student,
                subject=request.POST.get('subject'),
                date=request.POST.get('date'),
                defaults={
                    'status': request.POST.get('status'),
                    'marked_by': request.user
                }
            )

            messages.success(request, "Attendance marked!")
            return redirect('attendance')

        records = Attendance.objects.all().order_by('-date')

        return render(request, 'attendance.html', {
            'students': students,
            'records': records,
            'is_teacher': True
        })

    records = Attendance.objects.filter(student=request.user)

    total = records.count()
    present = records.filter(status='Present').count()

    return render(request, 'attendance.html', {
        'records': records,
        'percentage': round((present / total) * 100, 2) if total else 0,
        'total_classes': total,
        'present_count': present,
        'is_teacher': False
    })


# ================= NOTES =================
@login_required
def notes_view(request):
    notes = Note.objects.filter(user=request.user)
    return render(request, 'notes.html', {'notes': notes})


@login_required
def add_note(request):
    if request.method == "POST":
        Note.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            content=request.POST.get('content')
        )
    return redirect('notes')


@login_required
def delete_note(request, id):
    get_object_or_404(Note, id=id, user=request.user).delete()
    return redirect('notes')


# ================= TODO =================
@login_required
def todo_list(request):
    todos = Todo.objects.filter(user=request.user)
    return render(request, 'todo.html', {'todos': todos})


@login_required
def add_todo(request):
    if request.method == "POST":
        Todo.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            priority=request.POST.get('priority')
        )
    return redirect('todo')


@login_required
def complete_todo(request, pk):
    todo = get_object_or_404(Todo, id=pk, user=request.user)
    todo.is_completed = True
    todo.save()
    return redirect('todo')


@login_required
def delete_todo(request, pk):
    get_object_or_404(Todo, id=pk, user=request.user).delete()
    return redirect('todo')


# ================= ASSIGNMENT =================
@login_required
def assignment_home(request):

    if request.method == "POST":
        Assignment.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            subject=request.POST.get('subject'),
            description=request.POST.get('description'),
            due_date=request.POST.get('due_date')
        )
        return redirect('assignment_home')

    assignments = Assignment.objects.filter(user=request.user)
    return render(request, 'assignment.html', {'assignments': assignments})


@login_required
def delete_assignment(request, id):
    get_object_or_404(Assignment, id=id, user=request.user).delete()
    return redirect('assignment_home')


@login_required
def complete_assignment(request, id):
    assignment = get_object_or_404(Assignment, id=id, user=request.user)
    assignment.status = "Completed"
    assignment.save()
    return redirect('assignment_home')


 
# ================= TIMETABLE VIEW =================
# ================= TIMETABLE VIEW =================
@login_required
def timetable_view(request):
    data = Timetable.objects.all().order_by('day', 'start_time')
    return render(request, 'timetable.html', {'timetable': data})


# ================= ADD TIMETABLE =================
@login_required
def add_timetable(request):

    if not request.user.is_staff:
        return redirect('timetable')

    if request.method == "POST":
        Timetable.objects.create(
            class_name=request.POST.get('class_name'),
            subject=request.POST.get('subject'),
            day=request.POST.get('day'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
            room=request.POST.get('room')
        )
        return redirect('timetable')

    return render(request, 'add_timetable.html')


# ================= DELETE TIMETABLE =================
@login_required
def delete_timetable(request, id):

    if not request.user.is_staff:
        return redirect('timetable')

    get_object_or_404(Timetable, id=id).delete()
    return redirect('timetable')


# ================= EDIT TIMETABLE =================
@login_required
def edit_timetable(request, id):

    if not request.user.is_staff:
        return redirect('timetable')

    timetable = get_object_or_404(Timetable, id=id)

    if request.method == "POST":
        timetable.class_name = request.POST.get('class_name')
        timetable.subject = request.POST.get('subject')
        timetable.day = request.POST.get('day')
        timetable.start_time = request.POST.get('start_time')
        timetable.end_time = request.POST.get('end_time')
        timetable.room = request.POST.get('room')
        timetable.save()

        return redirect('timetable')

    return render(request, 'edit_timetable.html', {
        'timetable': timetable
    })