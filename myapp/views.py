from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import StudyMaterialForm

from .models import (
    Attendance,
    Note,
    Assignment,
    Submission,
    Timetable,
    Student,
    Exam,
    StudyMaterial
)

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

        title = request.POST.get('title')
        content = request.POST.get('content')
        pdf_file = request.FILES.get('pdf_file')

        # DEBUG (optional)
        print("TITLE:", title)
        print("PDF:", pdf_file)

        if title:   # important check
            Note.objects.create(
                user=request.user,
                title=title,
                content=content,
                pdf_file=pdf_file
            )

    return redirect('notes')


@login_required
def delete_note(request, id):
    note = get_object_or_404(Note, id=id, user=request.user)
    note.delete()
    return redirect('notes')

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
# ================= ADD STUDENT =================
@login_required
def add_student(request):

    if not request.user.is_staff:
        return redirect('home')

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        enrollment_no = request.POST.get('enrollment_no')

        course = request.POST.get('course')
        semester = request.POST.get('semester')

        # COMBINE COURSE + SEMESTER
        class_name = f"{course}-{semester}"

        # PREVENT DUPLICATE USERNAME
        if User.objects.filter(username=username).exists():

            messages.error(request, "Username already exists!")
            return redirect('add_student')

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

        messages.success(request, "Student added successfully!")

        return redirect('view_students')

    return render(request, 'add_student.html')


# ================= VIEW ALL STUDENTS =================
@login_required
def view_students(request):

    if not request.user.is_staff:
        return redirect('home')

    students = Student.objects.select_related(
        'user'
    ).all().order_by('-id')

    return render(request, 'view_students.html', {
        'students': students
    })


# ================= EDIT STUDENT =================
@login_required
def edit_student(request, pk):

    if not request.user.is_staff:
        return redirect('home')

    student = get_object_or_404(Student, id=pk)

    if request.method == "POST":

        username = request.POST.get('username')
        enrollment_no = request.POST.get('enrollment_no')

        course = request.POST.get('course')
        semester = request.POST.get('semester')

        # COMBINE COURSE + SEMESTER
        class_name = f"{course}-{semester}"

        # UPDATE USER
        student.user.username = username
        student.user.save()

        # UPDATE STUDENT
        student.enrollment_no = enrollment_no
        student.class_name = class_name

        student.save()

        messages.success(request, "Student updated successfully!")

        return redirect('view_students')

    return render(request, 'edit_student.html', {
        'student': student
    })


# ================= DELETE STUDENT =================
@login_required
def delete_student(request, pk):

    if not request.user.is_staff:
        return redirect('home')

    student = get_object_or_404(Student, id=pk)

    # DELETE USER
    # STUDENT AUTO DELETES DUE TO OneToOneField
    student.user.delete()

    messages.success(request, "Student deleted successfully!")

    return redirect('view_students')

    # ================= EXAM PLANNER =================
@login_required
def exam_list(request):
    exams = Exam.objects.all().order_by('exam_date')
    return render(request, 'examplanner/exam_list.html', {'exams': exams})


@login_required
def exam_create(request):
    if not request.user.is_staff:
        return redirect('exam_list')

    if request.method == "POST":
        Exam.objects.create(
            created_by=request.user,
            title=request.POST.get('title'),
            subject=request.POST.get('subject'),
            class_name=request.POST.get('class_name'),
            exam_date=request.POST.get('exam_date'),
            exam_time=request.POST.get('exam_time'),
            description=request.POST.get('description'),
        )
        return redirect('exam_list')

    return render(request, 'examplanner/exam_form.html')


@login_required
def exam_edit(request, pk):
    if not request.user.is_staff:
        return redirect('exam_list')

    exam = get_object_or_404(Exam, pk=pk)

    if request.method == "POST":
        exam.title = request.POST.get('title')
        exam.subject = request.POST.get('subject')
        exam.class_name = request.POST.get('class_name')
        exam.exam_date = request.POST.get('exam_date')
        exam.exam_time = request.POST.get('exam_time')
        exam.description = request.POST.get('description')
        exam.save()
        return redirect('exam_list')

    return render(request, 'examplanner/exam_form.html', {'exam': exam})


@login_required
def exam_delete(request, pk):
    if not request.user.is_staff:
        return redirect('exam_list')

    exam = get_object_or_404(Exam, pk=pk)

    if request.method == "POST":
        exam.delete()
        return redirect('exam_list')

    return render(request, 'examplanner/exam_confirm_delete.html', {'exam': exam})

# ================= NOTEBOOK VIEW =================

@login_required
def notebook_view(request):

    user = request.user

    # 👨‍🎓 STUDENT → ONLY THEIR COURSE + SEMESTER MATERIAL
    if not user.is_staff:
        try:
            student = user.student

            materials = StudyMaterial.objects.filter(
                course=student.course,
                semester=student.semester
            ).order_by('-created_at')

        except:
            materials = StudyMaterial.objects.none()

    # TEACHER : ONLY THEIR UPLOADED MATERIAL
    else:
        materials = StudyMaterial.objects.filter(
            uploaded_by=user
        ).order_by('-created_at')

    return render(request, 'notebook.html', {
        'materials': materials
    })


# ================= UPLOAD MATERIAL =================
@login_required
def upload_material(request):

    # ONLY TEACHERS CAN UPLOAD
    if not request.user.is_staff:
        return redirect('notebook')

    if request.method == 'POST':
        form = StudyMaterialForm(request.POST, request.FILES)

        if form.is_valid():
            material = form.save(commit=False)
            material.uploaded_by = request.user
            material.save()
            return redirect('notebook')

    else:
        form = StudyMaterialForm()

    return render(request, 'upload_material.html', {
        'form': form
    })


# ================= DELETE MATERIAL =================
@login_required
def delete_material(request, pk):

    material = get_object_or_404(StudyMaterial, id=pk)

    # ONLY OWNER TEACHER CAN DELETE
    if request.user != material.uploaded_by:
        return redirect('notebook')

    material.delete()
    return redirect('notebook')

 
  