from django.db import models
from django.contrib.auth.models import User


# timetable
class Timetable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="timetables")

    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    subject = models.CharField(max_length=100)
    time = models.CharField(max_length=50)

    class Meta:
        ordering = ['day']

    def __str__(self):
        return f"{self.user.username} | {self.day} | {self.subject}"


# attendance
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attendance_records")

    subject = models.CharField(max_length=100)
    total_classes = models.PositiveIntegerField(default=0)
    attended_classes = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'subject')
        ordering = ['subject']

    def percentage(self):
        if self.total_classes == 0:
            return 0
        return round((self.attended_classes / self.total_classes) * 100, 2)

    def is_low(self):
        return self.percentage() < 75

    def __str__(self):
        return f"{self.user.username} | {self.subject}"


# assignment
class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assignments")

    title = models.CharField(max_length=200)
    due_date = models.DateField()
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return self.title


# notes
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# todo
class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todos")

    task = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.task


# study tracker
class StudyTracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="study_logs")

    date = models.DateField()
    hours_studied = models.FloatField()

    class Meta:
        ordering = ['-date']


# exam planner
class ExamPlanner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exams")

    subject = models.CharField(max_length=100)
    exam_date = models.DateField()

    class Meta:
        ordering = ['exam_date']

    def __str__(self):
        return f"{self.subject} - {self.exam_date}"


# grades
class Grade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="grades")

    subject = models.CharField(max_length=100)
    marks = models.FloatField()

    def __str__(self):
        return f"{self.subject} - {self.marks}"


# library
class Library(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")

    book_name = models.CharField(max_length=200)
    issue_date = models.DateField()
    return_date = models.DateField()

    def __str__(self):
        return self.book_name


# events
class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")

    title = models.CharField(max_length=200)
    event_date = models.DateField()

    class Meta:
        ordering = ['event_date']

    def __str__(self):
        return self.title


# reminders
class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reminders")

    message = models.CharField(max_length=255)
    reminder_date = models.DateTimeField()

    class Meta:
        ordering = ['reminder_date']

    def __str__(self):
        return self.message