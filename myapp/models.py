from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator


class Timetable(models.Model):

    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    class_name = models.CharField(max_length=50)  # 👈 CLASS BASED (CSE-A, BCA-1)

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

    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )

    subject = models.CharField(max_length=100)

    date = models.DateField(
        default=timezone.now
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )

    marked_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='marked_attendance'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('student', 'subject', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.username} - {self.subject} - {self.status}"


# ================= ASSIGNMENT =================
class Assignment(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assignments"
    )

    title = models.CharField(max_length=200)

    subject = models.CharField(max_length=100)

    description = models.TextField(
        blank=True,
        null=True
    )

    due_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return f"{self.title} ({self.status})"


# ================= NOTES =================
class Note(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notes"
    )

    title = models.CharField(max_length=200)

    content = models.TextField()

    created_at = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# ================= TODO =================
class Todo(models.Model):

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="todos"
    )

    title = models.CharField(max_length=255)

    description = models.TextField(
        blank=True,
        null=True
    )

    is_completed = models.BooleanField(default=False)

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='MEDIUM'
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# ================= STUDY TRACKER =================
class StudyTracker(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="study_logs"
    )

    date = models.DateField(
        default=timezone.now
    )

    hours_studied = models.FloatField(
        validators=[MinValueValidator(0)]
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.hours_studied} hrs"


# ================= EXAM PLANNER =================
class ExamPlanner(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="exams"
    )

    subject = models.CharField(max_length=100)

    exam_date = models.DateField()

    class Meta:
        ordering = ['exam_date']

    def __str__(self):
        return f"{self.subject} - {self.exam_date}"


# ================= GRADES =================
class Grade(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="grades"
    )

    subject = models.CharField(max_length=100)

    marks = models.FloatField()

    class Meta:
        ordering = ['subject']

    def __str__(self):
        return f"{self.subject} - {self.marks}"


# ================= LIBRARY =================
class Library(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="books"
    )

    book_name = models.CharField(max_length=200)

    issue_date = models.DateField()

    return_date = models.DateField()

    class Meta:
        ordering = ['return_date']

    def __str__(self):
        return self.book_name


# ================= EVENTS =================
class Event(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="events"
    )

    title = models.CharField(max_length=200)

    event_date = models.DateField()

    class Meta:
        ordering = ['event_date']

    def __str__(self):
        return f"{self.title} - {self.event_date}"


# ================= REMINDERS =================
class Reminder(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reminders"
    )

    message = models.CharField(max_length=255)

    reminder_date = models.DateTimeField()

    class Meta:
        ordering = ['reminder_date']

    def __str__(self):
        return self.message