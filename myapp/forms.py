from django import forms
from .models import Timetable, Attendance, Assignment,StudyMaterial


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

#===============Notebook=================#
class StudyMaterialForm(forms.ModelForm):
    class Meta:
        model = StudyMaterial
        fields = ['title', 'description', 'file', 'course', 'semester']