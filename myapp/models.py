from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator
from datetime import date

#=======TIMETABLE==================#
class Timetable(models.Model):

    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    class_name = models.CharField(max_length=50)  #  CLASS BASED (CSE-A, BCA-1)

    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    subject = models.CharField(max_length=100)

    start_time = models.TimeField()
    end_time = models.TimeField()

    room = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['day', 'start_time']

    def __str__(self):
        return f"{self.class_name} | {self.day} | {self.subject}"

# ================= ATTENDANCE =================

class Attendance(models.Model):

    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
    ]

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    class_name = models.CharField(max_length=50)

    subject = models.CharField(max_length=100)

    date = models.DateField()

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES
    )

    marked_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='marked_attendance'
    )

    def __str__(self):
        return f"{self.student.username} - {self.subject} - {self.status}"

# ================= STUDENT =================
class Student(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    enrollment_no = models.CharField(max_length=50)

    class_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.class_name}"

# ================= ASSIGNMENT =================
class Assignment(models.Model):

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    title = models.CharField(max_length=200)

    class_name = models.CharField(max_length=100)

    subject = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    due_date = models.DateField()

    question_pdf = models.FileField(
        upload_to='assignments/',
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return date.today() > self.due_date

    def __str__(self):
        return self.title



# ================= SUBMISSION =================
class Submission(models.Model):

    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    solution_file = models.FileField(
        upload_to='solutions/'
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"

# ================= NOTES =================
class Note(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notes"
    )

    title = models.CharField(max_length=200)

    content = models.TextField(blank=True, null=True)

    # NEW: PDF SUPPORT
    pdf_file = models.FileField(
        upload_to='notes_pdfs/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

# ================= EXAM PLANNER =================

class Exam(models.Model):

    CLASS_CHOICES = [
        ('CSE-A', 'CSE-A'),
        ('CSE-B', 'CSE-B'),
        ('CIVIL', 'CIVIL'),
        ('MECH', 'MECH'),
    ]

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    class_name = models.CharField(max_length=20, choices=CLASS_CHOICES)

    exam_date = models.DateField()
    exam_time = models.TimeField()

    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ================= EVENTS =================
class Event(models.Model):
    message = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.message[:30]

#======Notebook============================#
class StudyMaterial(models.Model):

    COURSE_CHOICES = [
        ('BTECH', 'B.Tech'),
        ('BCA', 'BCA'),
        ('MCA', 'MCA'),
        ('MBA', 'MBA'),
    ]

    SEMESTER_CHOICES = [
        ('SEM1', 'Sem 1'),
        ('SEM2', 'Sem 2'),
        ('SEM3', 'Sem 3'),
        ('SEM4', 'Sem 4'),
        ('SEM5', 'Sem 5'),
        ('SEM6', 'Sem 6'),
        ('SEM7', 'Sem 7'),
        ('SEM8', 'Sem 8'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='study_materials/')

    course = models.CharField(max_length=10, choices=COURSE_CHOICES)
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)

    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

 