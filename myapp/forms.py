from django import forms
from .models import Timetable, Attendance, Assignment, StudyMaterial, Event 


# ================= TIMETABLE =================
class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = '__all__'


# ================= ATTENDANCE (MODEL-CORRECT SAFE VERSION) =================
class AttendanceForm(forms.ModelForm):

    # These are NOT stored in DB
    # Used only for UI filtering (course + semester selection)
    course = forms.ChoiceField(choices=[
        ('BTECH', 'B.Tech'),
        ('BCA', 'BCA'),
        ('MCA', 'MCA'),
        ('MBA', 'MBA'),
    ], required=False)

    semester = forms.ChoiceField(choices=[
        ('SEM1', 'Sem 1'),
        ('SEM2', 'Sem 2'),
        ('SEM3', 'Sem 3'),
        ('SEM4', 'Sem 4'),
        ('SEM5', 'Sem 5'),
        ('SEM6', 'Sem 6'),
        ('SEM7', 'Sem 7'),
        ('SEM8', 'Sem 8'),
    ], required=False)

    class Meta:
        model = Attendance
        fields = '__all__'   # IMPORTANT: keeps views.py SAFE


# ================= ASSIGNMENT =================
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = [
            'title',
            'course',
            'semester',
            'subject',
            'description',
            'due_date',
            'question_pdf'
        ]


# ================= STUDY MATERIAL =================
class StudyMaterialForm(forms.ModelForm):
    class Meta:
        model = StudyMaterial
        fields = ['title', 'description', 'file', 'course', 'semester']


# ================= EVENTS =================
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['message']