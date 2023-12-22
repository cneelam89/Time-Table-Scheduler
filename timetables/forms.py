from django.forms import ModelForm
from. models import *
from django import forms

class RoomForm(ModelForm):
    class Meta:
        model = Room
        labels = {"r_number": "Room ID", "seating_capacity": "Capacity"}
        fields = [ 'r_number','seating_capacity']
        widgets = {'r_number':forms.TextInput(attrs={'class':'form-control'}),
        'seating_capacity':forms.NumberInput(attrs={'class':'form-control'}), }


class ProfessorForm(ModelForm):
    class Meta:
        model = Professor
        labels = {"uid": "Professor UID", "name": "Full Name" }
        fields = ['uid','name' ]
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
        'uid':forms.TextInput(attrs={'class':'form-control'}), }


class ClassTimeForm(forms.ModelForm):
    class Meta:
        model = ClassTime
        fields = ['pid','time', 'day']
        labels = {'time': 'Time', 'day': 'Day of the Week'}
        widgets = {'pid':forms.TextInput(attrs={'class':'form-control'}),
            'time': forms.Select(),
            'day': forms.Select()
        }

    def clean(self):
        cleaned_data = super().clean()
        time = cleaned_data.get('time')
        day = cleaned_data.get('day')

        # Check if the selected time for the day already exists
        if ClassTime.objects.filter(time=time, day=day).exists():
            raise ValidationError("A class already exists for the selected time and day.")

        return cleaned_data


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['course_number', 'course_name', 'max_numb_students', 'professors']
        labels = {
            "course_number": "Course ID",
            "course_name": "Course Name",
            "max_numb_students": "Course Capacity",
            "professors": "Course Professors"
        }
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control'}),
            'course_number': forms.TextInput(attrs={'class': 'form-control'}),
            'max_numb_students': forms.TextInput(attrs={'class': 'form-control'}),
            'professors': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ['dept_name', 'courses']
        labels = {
            "dept_name": "Department Name",
            "courses": "Corresponding Courses"
        }
        widgets = {
            'dept_name': forms.TextInput(attrs={'class': 'form-control'}),
            'courses': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ['section_id', 'department', 'num_class_in_week']
        labels = {
            "section_id": "Section ID",
            "department": "Corresponding Department",
            "num_class_in_week": "Classes Per Week"
        }
        widgets = {
            'section_id': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'num_class_in_week': forms.TextInput(attrs={'class': 'form-control'}),
        }

