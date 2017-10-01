from django.views import generic
from .models import Client, Class, StripeInfo 
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from .forms import UserForm, UserEditForm, ClassForm, StudentForm, PhotoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import requests, json
from django.views.generic.edit import FormView
from django.http import HttpResponse
from django.shortcuts import render_to_response
import re
from django.views.generic.edit import UpdateView
import stripe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import csv
from cloudinary.forms import cl_init_js_callbacks  

#img upload
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django import forms
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt  

cloudinary.config( 
  cloud_name = "doeaevze5", 
  api_key = "938622343452691", 
  api_secret = "SyDTV3mGSJqfNrsHT7V2AZzJ8jU"
)



    
# Profile page for CMS    
@login_required(login_url='/manager/staff_login/') 
def profile(request):
    if not StripeInfo.objects.filter(user=request.user).exists():
        return redirect('/manager/stripe_setup', )
    else:    
        return render(request, 'profile.html')

# Stripe setup for new accounts
def stripe_setup(request):
    return render(request, 'registration/stripe_setup.html')
#------------------------------------------------------------- LIST VIEWS ------------------------------------------------------------------------


# Filter and list all classes by user/ organisation name    
@login_required(login_url='/manager/staff_login/')    
def classList(request):
    classes = Class.objects.filter(organisation_name = request.user)
    context={
        'classes':classes
    }
    return render(request, 'class/class_list.html', context)

# Filter and list all students by user/ org name
@login_required(login_url='/manager/staff_login/')
def studentList(request):
    name=''
    course=''
    students = Client.objects.filter(organisation_name = request.user)
    
    if request.GET:
        name = request.GET['name']
        course = request.GET['course']
    
    if name is not None and name != '':
        students = students.filter(name__icontains=name)
    
    if course is not None and course != '':
        students = students.filter(course__name__icontains=course)
    
    context = {
        'students': students,
        'name':name,
        'course': course
    }
    return render(request, 'student/student_list.html', context) 

#list of all classrooms for organisation       
def classroom_list(request):
    classrooms = ClassRoom.objects.filter(organisation_name = request.user)
    context = {
        'classrooms':classrooms,
    }
    return render(request, 'classroom/classroom_list.html', context)  

#user list       
def userList(request):
    users = Client.objects.filter(organisation_name = request.user)
    context = {
        'user':users,
    }
    return render(request, 'user_list.html', context) 

#class list view filtered by current classroom - might change to schedule view
def classroom_classlist(request, classroom_id):
    classroom = get_object_or_404(ClassRoom, pk=classroom_id)
    course = Class.objects.filter(class_room__pk=classroom_id)
    return render(request, 'classroom/classroom_classlist.html', {'course': course})


#----------------------------------------------------------- DETAIL VIEWS ---------------------------------------------------------------------

#detail view for classrooms
@login_required(login_url='/manager/staff_login/') 
def classroom_detail(request, classroom_id):
    user = request.user
    classroom = get_object_or_404(ClassRoom, pk=classroom_id)
    return render(request, 'classroom/classroom_detail.html', {'classroom': classroom, 'user': user, 'classroom_id': classroom_id})

#detail view for students
@login_required(login_url='/manager/staff_login/') 
def student_detail(request, student_id):
    student = get_object_or_404(Client, pk=student_id)
    return render(request, 'student/student_detail.html', {'student' : student})

#detail view for classes
@login_required(login_url='/manager/staff_login/')
def class_detail(request, class_id):
    course = get_object_or_404(Class, pk=class_id)
    pk = class_id;
    return render(request, 'class/class_detail.html', {'course': course, 'pk':pk})

#----------------------------------------------------------- ADD EDIT & DELETE VIEWS ----------------------------------------------------------

# Create classroom
@login_required(login_url='/manager/staff_login/')     
def create_classroom(request):
        form = ClassRoomForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.organisation_name = request.user.username
            classroom.save()
            classrooms = ClassRoom.objects.all()
            return redirect('/manager/classroom_list', )
        context = {
            "form": form,
        }
        return render(request, 'classroom/create_classroom.html', context)


# Edit classroom view        
def update_classroom(request, pk, template_name='classroom/update_classroom.html'):
    classroom = get_object_or_404(ClassRoom, pk=pk)
    img = classroom.image
    form = ClassRoomForm(request.POST or None, request.FILES or None, instance=classroom)
    if form.is_valid():
        
        if len(request.FILES) != 0:
            cloudinary.api.delete_resources([img])
        
        form.save()
        return redirect('/manager/classroom_list')
    return render(request, template_name, {'form':form})


# update class funtion
def update_class(request, pk, template_name='class/update_class.html'):
    course = get_object_or_404(Class, pk=pk)
    img = course.image
    form = ClassForm(request.POST or None, request.FILES or None, instance=course)
    if form.is_valid():
        
        if len(request.FILES) != 0:
            cloudinary.api.delete_resources([img])
        
        form.save()
        return redirect('/manager/class_list')
    return render(request, template_name, {'form':form, 'course': course})
    

# Edit student view        
class Update_Student(UpdateView):
    template_name = 'student/update_student.html'
    success_url = '/manager/student_list'
    model = Client
    fields = ['course', 'name', 'age', 'phone', 'gender', 'email'] 
        
# Create class   
@login_required(login_url='/manager/staff_login/') 
def create_class(request):
    form = ClassForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        course = form.save(commit = False)
        course.organisation_name = request.user.username
        #cloudinary.uploader.unsigned_upload(form.image, "unsigned_1", cloud_name = 'doeaevze5')
        course.save()
        return redirect('/manager/class_list', )
    context ={
        'form':form,
    }
    return render(request, 'class/create_class.html', context)

#create student    
@login_required(login_url='/manager/staff_login/') 
def create_student(request):
    form = StudentForm(request.POST or None)
    form.fields["course"].queryset = Class.objects.filter(organisation_name=request.user.username)
    if form.is_valid():
        student = form.save(commit = False)
        student.organisation_name = request.user.username
        student.save()
        return redirect('/manager/student_list', )
    context ={
        'form':form,
    }
    return render(request, 'student/create_student.html', context)

#delete student    
@login_required(login_url='/manager/staff_login/')    
def delete_student(request, student_id):
    current_user= request.user.username
    student = Client.objects.get(pk=student_id, organisation_name=current_user)
    student.delete()
    return redirect('student_list',)

# --------------------------------------------------------- USER VIEWS -----------------------------------------------------------------

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
                return redirect('/manager/staff_login', )
        else:
            return redirect('/manager/staff_login', )
    return render(request, 'registration/login.html')
    
#logout view
def logout_staff(request):
    logout(request)
    return redirect('/')

# get client stripe id using oauth    
def get_client_id(request):
    client_id = request.GET.get('code')
    current_user = request.user
    #test key to be changed for production!!!
    post_data = { 
       "client_secret":"sk_test_AgT7sGBgYum4cz1dr6H2BrNn",
       "code":client_id, 
       "grant_type":"authorization_code",
    }
    response = requests.post('https://connect.stripe.com/oauth/token', data=post_data)
    token = response.json().get('access_token')
    user_id = response.json().get('stripe_user_id')
    #get account and details
    info = stripe.Account.retrieve(user_id)
    country = info.get('country')
    city = info.get('city')
    
    context={
        'client_id':client_id,
        'token':token,
        'user_id': user_id
    }
    
    #check if stripe infor has been created for user
    count = StripeInfo.objects.filter(user=current_user).count()
    #create if non existent
    if count == 0:
        stripeInfo = StripeInfo.objects.create(user=current_user)
        stripeInfo.business_name = current_user.username
        stripeInfo.key = token
        stripeInfo.stripe_user_id = user_id
        stripeInfo.country = country
        stripeInfo.save()
    #edit otherwise
    else:
        stripeInfo = StripeInfo.objects.get(user=current_user)
        stripeInfo.business_name = current_user.username # might not need this
        stripeInfo.stripe_user_id = user_id
        stripeInfo.key = token
        stripeInfo.country = country
        stripeInfo.save()
    return render(request, 'test.html',context)




#csv function
def export_students(request):
    name=''
    course=''
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    
    students = Client.objects.filter(organisation_name = request.user)
    
    if request.GET:
        name = request.GET['name']
        course = request.GET['course']
    
    if name is not None and name != '':
        students = students.filter(name__icontains=name)
    
    if course is not None and course != '':
        students = students.filter(course__name__icontains=course)
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Age', 'Email', 'Phone'])
    
    for student in students:
        writer.writerow([student.name, student.age, student.email, student.phone])

    return response



#upload            
def upload_prompt(request):
  context = dict(direct_form = PhotoForm())
  cl_init_js_callbacks(context['direct_form'], request)
  
  return render(request, 'upload_prompt.html', context)

#upload complete  
@csrf_exempt
def direct_upload_complete(request):
  form = PhotoForm(request.POST)
  if form.is_valid():
    form.save()
    ret = dict(photo_id = form.instance.id)
  else:
    ret = dict(errors = form.errors)
    
  return HttpResponse(json.dumps(ret), content_type='application/json')