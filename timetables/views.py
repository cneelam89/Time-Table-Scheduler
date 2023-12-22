from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import *
from . forms import *
import random as rnd
from django.contrib import messages
from django.conf import settings
from django.views import View

MAX_GENERATIONS = 200
POPULATION_SIZE = 4
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 2
MUTATION_RATE = 0.02

class Data:
    def __init__(self):
        self._rooms = Room.objects.all()
        self._classTimes = ClassTime.objects.all()
        self._professors = Professor.objects.all()
        self._courses = Course.objects.all()
        self._depts = Department.objects.all()

    def get_rooms(self): return self._rooms

    def get_professors(self): return self._professors

    def get_courses(self): return self._courses

    def get_depts(self): return self._depts

    def get_classTimes(self): return self._classTimes


class Schedule:
    def __init__(self):
        self._data = data
        self._classes = []
        self._numberOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True
        self._used_rooms = set()
        self.professor_assignments = {}

    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes

    def get_numbOfConflicts(self):
        return self._numberOfConflicts

    def get_fitness(self):
        if self._isFitnessChanged:
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness

    def initialize(self):
        sections = Section.objects.all()
        available_rooms = list(data.get_rooms())
        class_times = sorted(data.get_classTimes(), key=lambda ct: ct.time)
        time_index = 0

        for section in sections:
            dept = section.department
            n = section.num_class_in_week
            if n <= len(ClassTime.objects.all()):
                courses = dept.courses.all()
                for course in courses:
                    crs_inst = course.professors.all()
                    if available_rooms:
                        room = available_rooms.pop(0)
                    else:
                        available_rooms = list(data.get_rooms())
                        room = available_rooms.pop(0)

                    for i in range(n // len(courses)):
                        newClass = Class(self._classNumb, dept, section.section_id, course)
                        self._classNumb += 1
                        newClass.set_classTime(class_times[time_index])
                        newClass.set_room(room)
                        self._used_rooms.add(room)
                        newClass.set_professor(crs_inst[rnd.randrange(0, len(crs_inst))])
                        self._classes.append(newClass)
                        time_index = (time_index + 1) % len(class_times)
            else:
                n = len(ClassTime.objects.all())
                courses = dept.courses.all()

                for course in courses:
                    crs_inst = course.professors.all()
                    if available_rooms:
                        room = available_rooms.pop(0)
                    else:
                        available_rooms = list(data.get_rooms())
                        room = available_rooms.pop(0)
                    for i in range(n // len(courses)):
                        newClass = Class(self._classNumb, dept, section.section_id, course)
                        self._classNumb += 1
                        newClass.set_classTime(class_times[time_index])
                        newClass.set_room(room)
                        self._used_rooms.add(room)
                        newClass.set_professor(crs_inst[rnd.randrange(0, len(crs_inst))])
                        self._classes.append(newClass)
                        time_index = (time_index + 1) % len(class_times)
        return self


    def calculate_fitness(self):
        self._numberOfConflicts = 0
        classes = self.get_classes()
        for i in range(len(classes)):
            if classes[i].room.seating_capacity < int(classes[i].course.max_numb_students):
                self._numberOfConflicts += 1
            for j in range(len(classes)):
                if j >= i:
                    if (classes[i].class_time.pid == classes[i].class_time.pid)  :
                        if classes[i].room == classes[j].room:
                            self._numberOfConflicts += 1
                        if classes[i].professor == classes[j].professor:
                            self._numberOfConflicts += 1
        return 1 / (1.0 * self._numberOfConflicts + 1)

class Population:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = [Schedule().initialize() for i in range(size)]

    def get_schedules(self):
        return self._schedules


class GeneticAlgorithm:
    def evolve(self, population):
        return self._mutate_population(self._crossover_population(population))

    def _crossover_population(self, pop):
        crossover_pop = Population(0)
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i = NUMB_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop

    def _mutate_population(self, population):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population

    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule().initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if rnd.random() > 0.5:
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule

    def _mutate_schedule(self, mutateSchedule):
        schedule = Schedule().initialize()
        for i in range(len(mutateSchedule.get_classes())):
            if MUTATION_RATE > rnd.random():
                mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule

    def _select_tournament_population(self, pop):
        tournament_pop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop


class Class:
    def __init__(self, id, dept, section, course):
        self.section_id = id
        self.department = dept
        self.course = course
        self.professor = None
        self.class_time = None
        self.room = None
        self.section = section

    def get_id(self): return self.section_id

    def get_dept(self): return self.department

    def get_course(self): return self.course

    def get_professor(self): return self.professor

    def get_classTime(self): return self.class_time

    def get_room(self): return self.room

    def set_professor(self, professor): self.professor = professor

    def set_classTime(self, classTime): self.class_time = classTime

    def set_room(self, room): self.room = room


data = Data()


def context_manager(schedule):
    classes = schedule.get_classes()
    context = []
    cls = {}
    for i in range(len(classes)):
        cls["section"] = classes[i].section_id
        cls['dept'] = classes[i].department.dept_name
        cls['course'] = f'{classes[i].course.course_name} ({classes[i].course.course_number}, ' \
                        f'{classes[i].course.max_numb_students}'
        cls['room'] = f'{classes[i].room.r_number} ({classes[i].room.seating_capacity})'
        cls['professor'] = f'{classes[i].professor.name} ({classes[i].professor.uid})'
        cls['class_time'] = [classes[i].class_time.pid, classes[i].class_time.day, classes[i].class_time.time]
        context.append(cls)
    return context


def timetable(request):
    schedule = []
    population = Population(POPULATION_SIZE)
    generation_num = 0
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    geneticAlgorithm = GeneticAlgorithm()
    while generation_num < MAX_GENERATIONS and population.get_schedules()[0].get_fitness() != 1.0:
        generation_num += 1
        print('\n> Generation #' + str(generation_num))
        print("Top Schedule Fitness:", population.get_schedules()[0].get_fitness())
        population = geneticAlgorithm.evolve(population)
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        schedule = population.get_schedules()[0].get_classes()

    return render(request, 'timetable.html', {'schedule': schedule, 'sections': Section.objects.all(),
                                              'times': ClassTime.objects.all()})
#######################
def index (request):
    return render(request, 'index.html')

def help(request):
    return render(request, 'help.html')


#### ######## professors ####### #######
def add_professors(request):
 if request.user.is_authenticated:
  if request.method == 'POST':
   form = ProfessorForm(request.POST)
   if form.is_valid():
    form.save()
    form = ProfessorForm()
    messages.success(request, 'added in Successfully !!')
  else:
   form = ProfessorForm()
  return render(request, 'addProfessor.html', {'form':form})
 else:
  return HttpResponseRedirect('/accounts/login/')


@login_required
def edit_professors(request):
    professors= Professor.objects.all()
    return render(request, 'editProfessor.html', {'data':professors})


@login_required
def delete_professors(request, id):
    if request.method == 'POST':
      pi = Professor.objects.get(pk=id)
      pi.delete()
      return HttpResponseRedirect('/')



#### ######## room ####### #######
@login_required
def addRooms(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'added in Successfully !!')
            form = RoomForm()
            # return redirect('addRooms')
    return render(request, 'addRooms.html', {'form':form})


@login_required
def room_list(request):
    rooms=Room.objects.all()
    return render(request, 'roomslist.html', {'rooms':rooms})

@login_required
def delete_room(request, id):
    rm = Room.objects.filter(pk=id)
    if request.method == 'POST':
        rm.delete()
        return HttpResponseRedirect('/')


#### ######## time ####### #######
@login_required
def addTimings(request):
    form = ClassTimeForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            form = ClassTimeForm()  # Reset the form after successful save
    return render(request, 'addTimings.html', {'form': form})


@login_required
def edit_class_time(request):
        class_time= ClassTime.objects.all()
        return render(request, 'editclasstime.html',{'class_time':class_time})

@login_required
def delete_class_time(request, id):
    cl = ClassTime.objects.get(pk=id)
    if request.method == 'POST':
        cl.delete()
        return HttpResponseRedirect('/')

#### ######## courses ####### #######
@login_required
def addCourses(request):
    form = CourseForm()
    if request.method == 'POST':
        form = CourseForm(request.POST or None)
        if form.is_valid():
            form.save()
            form = CourseForm()
            messages.success(request, 'added in Successfully !!')
        else:
            form = ProfessorForm()
    return render(request, 'addCourses.html', {'form':form})

@login_required
def course_list_view(request):
        courses=Course.objects.all()
        return render(request, 'editcourses.html', {'courses':courses})

@login_required
def delete_course(request, pk):
    crs = Course.objects.filter(pk=pk)
    if request.method == 'POST':
        crs.delete()
        return HttpResponseRedirect('/')


#### ######## departments ####### #######
@login_required
def addDepts(request):
    form = DepartmentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            form = DepartmentForm()
            messages.success(request, 'added in Successfully !!')
        else:
            form = DepartmentForm()
    return render(request, 'addDepts.html',{'form':form})

@login_required
def department_list(request):
    departments= Department.objects.all()
    return render(request, 'editdept.html', {'departments':departments})

@login_required
def delete_department(request, pk):
    dept = Department.objects.filter(pk=pk)
    if request.method == 'POST':
        dept.delete()
        return HttpResponseRedirect('/')


#### ######## sections ####### #######
@login_required
def addSections(request):
    form = SectionForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            form = SectionForm()
            messages.success(request, 'added in Successfully !!')
        else:
            form = SectionForm()
    return render(request, 'addSections.html', {'form':form})

@login_required
def section_list(request):
    sections= Section.objects.all()
    return render(request, 'editsection.html', {'sections':sections})

@login_required
def delete_section(request, pk):
    sec = Section.objects.filter(pk=pk)
    if request.method == 'POST':
        sec.delete()
        return HttpResponseRedirect('/')



