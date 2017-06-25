from django.views import generic
from .models import ClassRoom, Client, Class 
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from .forms import UserForm, UserEditForm, ClassRoomForm, ClassForm, StudentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def index(request):
    return render(request, 'index.html')
    
@login_required(login_url='/manager/staff_login/') 
def profile(request):
    return render(request, 'profile.html')

class ClassListView(generic.ListView):
    template_name= "class/class_list.html"
    
    def get_queryset(self):
        return Class.objects.all()

class StudentListView(generic.ListView):
    template_name= "student/student_list.html"
    
    def get_queryset(self):
        return Client.objects.all()

#list of all classrooms        
class ClassRoomListView(generic.ListView):
    template_name= "classroom/classroom_list.html"
    
    def get_queryset(self):
        return ClassRoom.objects.all()  

#List of all registered users        
class UserListView(generic.ListView):
    template_name= "user_list.html"
    
    def get_queryset(self):
        return User.objects.all() 

#detail view for students
@login_required(login_url='/manager/staff_login/') 
def student_detail(request, student_id):
    student = get_object_or_404(Client, pk=student_id)
    return render(request, 'student/student_detail.html', {'student' : student})

#detail view for classes
@login_required(login_url='/manager/staff_login/')
def class_detail(request, class_id):
    course = get_object_or_404(Class, pk=class_id)
    return render(request, 'class/class_detail.html', {'course': course})

#class list view filtered by current classroom - might change to schedule view
def classroom_classlist(request, classroom_id):
    classroom = get_object_or_404(ClassRoom, pk=classroom_id)
    course = Class.objects.filter(class_room__pk=classroom_id)
    return render(request, 'classroom/classroom_classlist.html', {'course': course})

#detail view for classrooms
@login_required(login_url='/manager/staff_login/') 
def classroom_detail(request, classroom_id):
        user = request.user
        classroom = get_object_or_404(ClassRoom, pk=classroom_id)
        return render(request, 'classroom/classroom_detail.html', {'classroom': classroom, 'user': user, 'classroom_id': classroom_id})

#register new users for cms
def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/manager/profile', )
    context = {
        "form": form,
    }
    return render(request, 'register.html', context)

#view for creating classroom 
@login_required(login_url='/manager/staff_login/')     
def create_classroom(request):
        form = ClassRoomForm(request.POST or None)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.user = request.user
            classroom.save()
            classrooms = ClassRoom.objects.all()
            return redirect('/manager/classroom_list', )
        context = {
            "form": form,
        }
        return render(request, 'classroom/create_classroom.html', context)
        
#view for creating a class - from classroom        
@login_required(login_url='/manager/staff_login/') 
def create_class(request):
    form = ClassForm(request.POST or None)
    if form.is_valid():
        course = form.save(commit = False)
        course.save()
        return redirect('/manager/class_list', )
    context ={
        'form':form,
    }
    return render(request, 'class/create_class.html', context)

#create a student    
@login_required(login_url='/manager/staff_login/') 
def create_student(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        student = form.save(commit = False)
        student.save()
        return redirect('/manager/student_list', )
    context ={
        'form':form,
    }
    return render(request, 'student/create_student.html', context)

#delete student    
@login_required(login_url='/manager/staff_login/')    
def delete_student(request, student_id):
    student = Client.objects.get(pk=student_id)
    student.delete()
    return redirect('student_list', )
    
#login view
def login_staff(request):
    #check to see if user is a client
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.groups.filter(name__in=['customer']).exists():
                return redirect('/portal/customer_login/')
            elif user.is_active:
                login(request, user)
                return redirect('/manager/profile', )
            else:
                return redirect('/manger/staff_login', )
        else:
            return redirect('/manager/staff_login', )
    return render(request, 'registration/login.html')
    
#Logout view
def logout_staff(request):
    logout(request)
    return redirect('/manager/staff_login')