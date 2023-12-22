

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('help/', views.help, name='help'),
    path('add_professors/', views.add_professors, name='add_professors'),
    path('edit_professors/', views.edit_professors , name='edit_professors'),
    path('delete_professors/<int:id>/', views.delete_professors, name='deleteprofessors'),
    path('add_rooms', views.addRooms, name='addRooms'),
    path('rooms_list/', views.room_list, name='editrooms'),
    path('delete_room/<int:id>/', views.delete_room, name='deleteroom'),
    path('add_timings', views.addTimings, name='addTimings'),
    path('timings_list/', views.edit_class_time, name='editclassime'),
    path('delete_classtime/<int:id>/', views.delete_class_time, name='deleteclasstime'),
    path('add_courses', views.addCourses, name='addCourses'),
    path('courses_list/', views.course_list_view, name='editcourse'),
    path('delete_course/<str:pk>/', views.delete_course, name='deletecourse'),
    path('add_departments', views.addDepts, name='addDepts'),
    path('departments_list/', views.department_list, name='editdepartment'),
    path('delete_department/<int:pk>/', views.delete_department, name='deletedepartment'),
    path('add_sections', views.addSections, name='addSections'),
    path('sections_list/', views.section_list, name='editsection'),
    path('delete_section/<str:pk>/', views.delete_section, name='deletesection'),
    path('timetable_generation/', views.timetable, name='timetable'),
]
