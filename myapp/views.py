from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Attendance, Note, Todo, Assignment, Submission, Timetable, Student


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

 
## ================= ATTENDANCE =================
@login_required
def attendance_view(request):

    is_teacher = request.user.is_staff

    # SHOW ALL STUDENTS INITIALLY
    students = Student.objects.all()

    # ================= STAFF SIDE =================
    if request.method == "POST" and is_teacher:

        class_name = request.POST.get('class_name')
        subject = request.POST.get('subject')
        date = request.POST.get('date')

        # LOAD ONLY SELECTED CLASS STUDENTS
        students = Student.objects.filter(
            class_name=class_name
        )

        # SAVE ATTENDANCE
        for student in students:

            status = request.POST.get(
                f'student_{student.user.id}'
            )

            # SAVE ONLY IF PRESENT/ABSENT SELECTED
            if status:

                Attendance.objects.create(
                    student=student.user,
                    class_name=class_name,
                    subject=subject,
                    date=date,
                    status=status,
                    marked_by=request.user
                )

        return redirect('attendance')

    # ================= TEACHER VIEW =================
    if is_teacher:

        records = Attendance.objects.all().order_by('-date')

        total_classes = 0
        present_count = 0
        percentage = 0

    # ================= STUDENT VIEW =================
    else:

        records = Attendance.objects.filter(
            student=request.user
        ).order_by('-date')

        total_classes = records.count()

        present_count = records.filter(
            status='P'
        ).count()

        percentage = (
            round((present_count / total_classes) * 100, 2)
            if total_classes > 0 else 0
        )

    return render(request, 'attendance.html', {

        'is_teacher': is_teacher,

        'students': students,

        'records': records,

        'total_classes': total_classes,

        'present_count': present_count,

        'percentage': percentage,
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


# ================= ASSIGNMENT PAGE =================
@login_required
def assignment_view(request):

    is_teacher = request.user.is_staff

    # ================= TEACHER SIDE =================
    if is_teacher:

        if request.method == "POST":

            title = request.POST.get('title')
            class_name = request.POST.get('class_name')
            subject = request.POST.get('subject')
            description = request.POST.get('description')
            due_date = request.POST.get('due_date')

            question_pdf = request.FILES.get('question_pdf')

            Assignment.objects.create(
                teacher=request.user,
                title=title,
                class_name=class_name,
                subject=subject,
                description=description,
                due_date=due_date,
                question_pdf=question_pdf
            )

            return redirect('assignment')

        assignments = Assignment.objects.all().order_by('-created_at')

    # ================= STUDENT SIDE =================
    else:

        student_class = request.user.student.class_name

        assignments = Assignment.objects.filter(
            class_name=student_class
        ).order_by('-created_at')

    return render(request, 'assignment.html', {
        'assignments': assignments,
        'is_teacher': is_teacher
    })



# ================= SUBMIT ASSIGNMENT =================
@login_required
def submit_assignment(request, assignment_id):

    assignment = get_object_or_404(
        Assignment,
        id=assignment_id
    )

    # STOP AFTER LAST DATE
    if assignment.is_expired():
        return redirect('assignment')

    if request.method == "POST":

        solution_file = request.FILES.get('solution_file')

        Submission.objects.create(
            assignment=assignment,
            student=request.user,
            solution_file=solution_file
        )

    return redirect('assignment')



# ================= VIEW SUBMISSIONS =================
@login_required
def view_submissions(request, assignment_id):

    assignment = get_object_or_404(
        Assignment,
        id=assignment_id
    )

    submissions = Submission.objects.filter(
        assignment=assignment
    )

    return render(request, 'submissions.html', {
        'assignment': assignment,
        'submissions': submissions
    })



# ================= DELETE ASSIGNMENT =================
@login_required
def delete_assignment(request, assignment_id):

    assignment = get_object_or_404(
        Assignment,
        id=assignment_id
    )

    assignment.delete()

    return redirect('assignment')
 
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

    # ================= Student =================
@login_required
def add_student(request):

    if not request.user.is_staff:
        return redirect('home')

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        enrollment_no = request.POST.get('enrollment_no')
        class_name = request.POST.get('class_name')

        # CREATE USER
        user = User.objects.create_user(
            username=username,
            password=password
        )

        # CREATE STUDENT PROFILE
        Student.objects.create(
            user=user,
            enrollment_no=enrollment_no,
            class_name=class_name
        )

        return redirect('add_student')

    return render(request, 'add_student.html')