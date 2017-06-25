from django.shortcuts import render
from django.views import generic
from manager.models import  Class, ClientProfile, Client 
from django.contrib.auth import login, authenticate, logout
from .forms import CustomerForm, CustomerEditForm, StudentForm, StudentProfileForm
from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
import stripe
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY

#index view
def index(request):
    return render(request, 'portal_index.html')

#login view
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/portal/customer_profile', )
            else:
                return redirect('/portal/customer_login', )
        else:
            return redirect('/portal/customer_login', )
    return render(request, 'registration/customer_login.html')
    
#Logout view
def logout_user(request):
    logout(request)
    return redirect('/portal/customer_login')

#Create your views here.
class ClassListView(generic.ListView):
    template_name= "customer_class/class_list.html"
    
    def get_queryset(self):
        return Class.objects.all()

#detail view for students
@login_required(login_url='/portal/customer_login/')
def class_detail(request, class_id):
    course = get_object_or_404(Class, pk=class_id)
    students = ClientProfile.objects.filter(user=request.user)

    return render(request, 'customer_class/class_detail.html', {'course' : course, 'students':students})        

#Customer profile
@login_required(login_url='/portal/customer_login/')
def customer_profile(request):
    return render(request, 'customer/customer_profile.html')

#Registration for customers
def register(request):
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
                return redirect('customer_profile', )
    context = {
        "form": form,
    }
    return render(request, 'registration/register.html', context)
    
#create a student profile    
@login_required(login_url='/portal/customer_login/')
def create_student(request):
    form = StudentProfileForm(request.POST or None)
    if form.is_valid():
        student = form.save(commit=False)
        student.user = request.user
        student = form.save()
        return redirect('customer_profile')
        #return render(request, 'registration/checkout.html', {'student': student, 'course':course})
    context ={
        'form':form,
    }
    return render(request, 'student/create_student.html', context)
    
#credit card processing   
def checkout(request, class_id, student_id):
    course = get_object_or_404(Class, pk=class_id)
    student = get_object_or_404(ClientProfile, pk=student_id)
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        token = request.POST['stripeToken']
        try:
        # Use Stripe's library to make requests...
        # Charge the user's card:
            charge = stripe.Charge.create(
                amount=1500,
                currency="cad",
                description="Example charge",
                receipt_email= "magnejulien@hotmail.com",
                source=token,
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
            #make copy of student profile if no errors
            u = Client.objects.create(course=course, name=student.name, age=student.age, phone=student.phone, gender=student.gender, email=student.email)
            u.save()
    context = {'publishKey': publishKey}
    template = 'registration/checkout.html'
    return render(request, template, context)
    
