from django.contrib.auth.models import User
from manager.models import Class, Client
from django import forms
import datetime, calendar
from django.forms import ModelForm, Textarea
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import TabHolder, Tab
from .models import Photo

class PhotoForm(ModelForm):
  class Meta:
      model = Class
      fields = ['image']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        
class DateInput(forms.DateInput):
    input_type = 'date'
    
class TimeInput(forms.TimeInput):
    input_type = 'time'
    
class ClassForm(forms.ModelForm):
    description = forms.CharField( widget=forms.Textarea )
    helper = FormHelper()
    helper.form_tag = False
    #city = models.CharField(max_length=50)
    #address = models.CharField(max_length = 100)
    #phone_number = models.IntegerField(null=True, blank=True);
    
    
    helper.layout = Layout(
        TabHolder(
            Tab(
                'Basic Information',
                'name','teacher',
                'capacity','price','description','image'  
            ),
            Tab(
                'Time',
                'start_time',
                'end_time',
                'start_date',
                'end_date',
                'monday', 
                'tuesday',
                'wednesday',
                'thursday',
                'friday',
                'saturday', 
                'sunday'
            ),
            Tab(
                'Contact',
                'address','phone_number'
            )
        )   
    )
    
    class Meta:
        model = Class
        fields = [ 'name','teacher','start_time',
        'end_time','capacity','price','description', 'start_date', 
        'end_date','monday', 'tuesday','wednesday','thursday',
        'friday','saturday', 'sunday','image','address', 'phone_number']
        widgets = {
            'start_date': DateInput(),
            'start_time': TimeInput(),
            'end_date': DateInput(),
            'end_time': TimeInput(),
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['course', 'name','last_name','age', 'phone', 'gender', 'email', 'address']    
        
        

class NoFormTagCrispyFormMixin(object):
    @property
    def helper(self):
        if not hasattr(self, '_helper'):
            self._helper = FormHelper()
            self._helper.form_tag = False
        return self._helper
        
