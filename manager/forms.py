from django.contrib.auth.models import User
from models import ClassRoom, Class, Client
from django import forms
import datetime, calendar
from django.forms import ModelForm, Textarea


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        
class ClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoom
        fields = ['name', 'location']

class DateInput(forms.DateInput):
    input_type = 'date'
    
class TimeInput(forms.TimeInput):
    input_type = 'time'
    
class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['class_room','name','teacher','start_time',
        'end_time','capacity','price','description', 'start_date', 
        'end_date','monday', 'tuesday','wednesday','thursday',
        'friday','saturday', 'sunday']
        widgets = {
            'start_date': DateInput(),
            'start_time': TimeInput(),
            'end_date': DateInput(),
            'end_time': TimeInput(),
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['course', 'name', 'age', 'phone', 'gender', 'email']    
        
        
