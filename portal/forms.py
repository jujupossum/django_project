from django.contrib.auth.models import User
from manager.models import Class, Client, ClientProfile
from django import forms


class CustomerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
class CustomerEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        
class StudentForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['course', 'name', 'age', 'phone', 'gender', 'email']
        
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['name', 'age', 'phone', 'gender', 'email']