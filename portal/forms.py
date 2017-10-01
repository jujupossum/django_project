from django.contrib.auth.models import User
from manager.models import Class, Client, ClientProfile
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import TabHolder, Tab

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
        fields = ['name','last_name', 'age', 'phone', 'gender', 'email', 'address']
        


class NoFormTagCrispyFormMixin(object):
    @property
    def helper(self):
        if not hasattr(self, '_helper'):
            self._helper = FormHelper()
            self._helper.form_tag = False
        return self._helper
        
