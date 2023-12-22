from django.contrib import admin
from .models import Room, Professor, ClassTime, Course, Department, Section

# Register your models here.

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['r_number', 'seating_capacity']

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['uid', 'name']

@admin.register(ClassTime)
class ClassTimeAdmin(admin.ModelAdmin):
    list_display = ['pid', 'time', 'day', 'duration']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_number', 'course_name', 'max_numb_students']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['dept_name']

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['section_id', 'department', 'num_class_in_week', 'course', 'class_time', 'room', 'professor']
    list_filter = ['department', 'course', 'class_time', 'room', 'professor']
