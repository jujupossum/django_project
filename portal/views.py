from django.shortcuts import render
from django.views import generic
from manager.models import  Class, ClientProfile, Client, StripeInfo, ClassHistory 
from django.contrib.auth import login, authenticate, logout
from .forms import CustomerForm, CustomerEditForm, StudentForm, StudentProfileForm
from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
import datetime
import stripe
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.apps import AppConfig
import requests
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

stripe.api_key = settings.STRIPE_SECRET_KEY

# Index view
class Index(generic.ListView):
    template_name= "portal_index.html"
    
    def get_queryset(self):
        return User.objects.filter(groups__name='customer')
    
# login view
def login_user(request):
    state = "Please log in below..."
    username = password = ''
    next = ""
    if request.GET:  
        next = request.GET['next']

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
                if next == "":
                    return HttpResponseRedirect('/portal/default/class_list')
                else:
                    return HttpResponseRedirect(next)
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    return render_to_response(
        'registration/customer_login.html',
        {
        'state':state,
        'username': username,
        'next':next,
        },
        context_instance=RequestContext(request)
    )
    
# Logout view
def logout_user(request):
    logout(request)
    return redirect('/portal/customer_login')

# Class list view 
@login_required(login_url='/portal/customer_login/')
def classList(request, organisation):
    name = ''
    
    if request.GET:
        name = request.GET['name']    
    
    organisation= organisation;
    template_name= "customer_class/class_list.html"
    classes = Class.objects.filter(organisation_name = organisation)
    
    if name is not None and name != '':
        classes = classes.filter(name__icontains=name)

    context={
    'organisation':organisation,
    'classes':classes,
    }
    return render(request, template_name, context)

# Detail view for classes
def class_detail(request, class_id, organisation):
    course = get_object_or_404(Class, pk=class_id)
    context={
        'course':course,
        'organisation': organisation,
    }
    return render(request, 'customer_class/class_detail.html', context)        

# Class history
@login_required(login_url='/portal/customer_login/')
def class_history(request):
    classes = ClassHistory.objects.filter(user = request.user)
    return render(request, 'customer_class/class_history.html', {'classes':classes})

# Customer profile
@login_required(login_url='/portal/customer_login/')
def customer_profile(request):
    return render(request, 'customer/customer_profile.html')

# Registration for customers
def register(request):
     
    if request.GET:  
        next = request.GET['next']
    
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                group = Group.objects.get_or_create(name='customer')[0] 
                user.groups.add(group)
                login(request, user)
                if next == "":
                    return HttpResponseRedirect('/customer_profile/')
                else:
                    return HttpResponseRedirect(next)
    context = {
        "form": form,
    }
    return render(request, 'registration/register.html', context)
    
# Register student information before payment  
@login_required(login_url='/portal/customer_login/')
def create_student_profile(request, organisation, class_id):
    course = get_object_or_404(Class, pk=class_id)
    form = StudentProfileForm(request.POST or None)
    if form.is_valid():
        student = form.save(commit=False)
        student.user = request.user
        student.organisation = organisation
        student.course_id = class_id
        student = form.save()
        return redirect( 'checkout')
    context ={
        'form':form,
        'course':course
    }
    return render(request, 'customer_student/create_student.html', context)
    
# Credit card processing   
def checkout(request):
    student = get_object_or_404(ClientProfile, user = request.user)
    course = get_object_or_404(Class, pk=student.course_id, organisation_name = student.organisation)
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    stripe_info = get_object_or_404(StripeInfo, business_name = student.organisation)
    current_user = request.user
    
    if request.method == 'POST':
        token = request.POST['stripeToken']
        try:
        # Use Stripe's library to make requests...
        # Charge the user's card:
            charge = stripe.Charge.create(
                amount=course.price,
                currency="cad",
                description="Example charge",
                receipt_email= "magnejulien@hotmail.com",
                source=token,
                application_fee=123,
                stripe_account=stripe_info.stripe_user_id,
            )
            pass
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err  = body['error']
            print "Status is: %s" % e.http_status
            print "Type is: %s" % err['type']
            print "Code is: %s" % err['code']
            # param is '' in this case
            print "Param is: %s" % err['param']
            print "Message is: %s" % err['message']
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            pass
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            pass
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            pass
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            pass
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            pass
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            pass
        else:
            # Make copy of student profile if no errors and add to client database
            u = Client.objects.create(course=course, organisation_name=course.organisation_name, name=student.name, age=student.age, phone=student.phone, gender=student.gender, email=student.email, address = student.address)
            u.save()
            j = ClassHistory.objects.create(user = current_user ,class_name = course.name, registered_date = datetime.datetime.now(), organisation_name = course.organisation_name, 
            name = course.name, teacher = course.teacher, start_time = course.start_time, end_time = course.end_time, start_date = course.start_date, end_date = course.end_date, description = course.description,
            price = course.price, image = course.image, address = course.address, phone_number = course.phone_number            
            )
            j.save()
            return render(request, 'customer_class/class_history.html')            
    context = {'publishKey': publishKey,
               'course' : course,
               'student': student
    }
    template = 'registration/checkout.html'
    return render(request, template, context)
    

#filter class objects         
def search(request):
    text=''
    city=''
    errors = []
    if 'text' in request.GET:
        text = request.GET['text']
        city = request.GET['city']
        if text is not None and text != '': 
            class_list = Class.objects.filter(
                name__icontains=text
            ).filter(
                address__icontains=city
            )
            query = "text: %s, city: %s" % (text, city)
            #--------------------PAGINATOR------------------------------------
            paginator = Paginator(class_list, 12) # Show 25 contacts per page

            page = request.GET.get('page')
            try:
                classes = paginator.page(page)
            except PageNotAnInteger:
            # If page is not an integer, deliver first page.
                classes = paginator.page(1)
            except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
                classes = paginator.page(paginator.num_pages)
            context ={'classes': classes, 'query': query, 'city':city, 'text':text}    
            return render_to_response('customer_class/class_search.html', context)
        
        
        else:
            class_list = Class.objects.filter(address__icontains=city)
            query = "text: %s, city: %s" % (text, city)
            #--------------------PAGINATOR------------------------------------
            paginator = Paginator(class_list, 12) # Show 25 contacts per page

            page = request.GET.get('page')
            try:
                classes = paginator.page(page)
            except PageNotAnInteger:
            # If page is not an integer, deliver first page.
                classes = paginator.page(1)
            except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
                classes = paginator.page(paginator.num_pages)
            context ={'classes': classes, 'query': query, 'city':city, 'text':text}
            return render_to_response('customer_class/class_search.html',context)
            
    return render_to_response('customer_class/class_search.html',
            {'errors': errors})        
