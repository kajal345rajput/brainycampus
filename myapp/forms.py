from django import forms
from .models import Timetable, Attendance, Assignment


class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = '__all__'


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = '__all__'