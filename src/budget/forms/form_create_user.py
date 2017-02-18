'''
Created on Aug 20, 2014

@author: thavr
'''

from django import forms
from budget.models import Family
from django.contrib.auth.models import User
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.forms.utils import ErrorList
from captcha.fields import CaptchaField

class CreateUserForm(forms.Form):
    email = forms.EmailField(label="Email Address* ", \
                             widget=forms.EmailInput(attrs={\
                                 'autocomplete':'off', \
                                 'placeholder':'email', \
                                 'tabindex':'1', \
                                 'id':'email', \
                                 'title':'Your address for e-mails by ' + \
                                 'default it will be your username as well.', \
                                 'required':''}))
    password = forms.CharField(label="Password* ", \
                               widget = forms.PasswordInput(attrs={\
                                 'autocomplete':'off', \
                                 'placeholder':'password', \
                                 'tabindex':'2', \
                                 'id':'password', \
                                 'title':'Type desirable password here', \
                                 'required':''}))
    retypepassword = forms.CharField(label="Retype password* ", \
                                     widget = forms.PasswordInput(attrs={\
                                     'autocomplete':'off', \
                                     'placeholder':'retype password', \
                                     'tabindex':'3', \
                                     'id':'retypepassword', \
                                     'title':'Retype your desirable password', \
                                     'required':''}))
    family_email = forms.EmailField(required=False, \
                                    label="Any Family?",\
                                    widget=forms.EmailInput(attrs={\
                                     'autocomplete':'off', \
                                     'placeholder':'family email', \
                                     'tabindex':'4', \
                                     'id':'family_email', \
                                     'title':'Email of any member of the ' + \
                                     'family you are the part of'}))
    fname = forms.CharField(required=False, \
                            label="First Name", \
                            widget = forms.TextInput(attrs={\
                             'autocomplete':'off', \
                             'placeholder':'first name', \
                             'tabindex':'5', \
                             'id':'fname', \
                             'title':'Your first name'}))
    sname = forms.CharField(required=False, \
                            label="Last Name", \
                            widget = forms.TextInput(attrs={\
                             'autocomplete':'off', \
                             'placeholder':'last name', \
                             'tabindex':'6', \
                             'id':'sname', \
                             'title':'Your last name'}))
    birthdate = forms.CharField(required=False, localize=True, \
                                label="Birthdate", \
                            widget = forms.DateInput(attrs={\
                             'autocomplete':"off", 'type':'date', \
                             'id':"birthdate", \
#                             'readonly':'', \
                             'value':"", \
                             'title':"When were you born?", \
                             'onclick':"displayCalendar(document.forms[0].birthdate, 'dd.mm.yyyy', this)"}))
    cellcountry = forms.CharField(required=False, \
                                  label="Country Code for cell phone", \
                                  widget=forms.TextInput(attrs={\
                                    'autocomplete':'off', \
                                    'placeholder':'country code', \
                                    'tabindex':'9', \
                                    'id':'cellcountry', \
                                    'title':'Country code of your cell phone'}))
    cellarea = forms.CharField(required=False, \
                               label="Area Code for cell phone", \
                                  widget=forms.TextInput(attrs={\
                                    'autocomplete':'off', \
                                    'placeholder':'area code', \
                                    'tabindex':'10', \
                                    'id':'cellarea', \
                                    'title':'Area code of your cell phone'}))
    cellnumber = forms.CharField(required=False, \
                                 label="Cell phone number", \
                                  widget=forms.TextInput(attrs={\
                                    'autocomplete':'off', \
                                    'placeholder':'cell number', \
                                    'tabindex':'11', \
                                    'id':'cellnumber', \
                                    'title':'Dialing number of your cell phone'}))
    addrcountry = forms.CharField(required=False, \
                                  label="Country", \
                                  widget=forms.TextInput(attrs={\
                                    'autocomplete':'off', \
                                    'placeholder':'country', \
                                    'tabindex':'12', \
                                    'id':'addrcountry', \
                                    'title':'Country where you live'}))
    addrpostid = forms.CharField(required=False, \
                                 label="Zip code", \
                                  widget=forms.TextInput(attrs={\
                                    'autocomplete':'off', \
                                    'placeholder':'zip code', \
                                    'tabindex':'13', \
                                    'id':'addrpostid', \
                                    'title':'Your postal code'}))
    addrcity = forms.CharField(required=False, \
                               label="City/Town", \
                                  widget=forms.TextInput(attrs={\
                                    'autocomplete':'off', \
                                    'placeholder':'city', \
                                    'tabindex':'14', \
                                    'id':'addrcity', \
                                    'title':'City or town where you live'}))
    addrstr = forms.CharField(required=False, \
                              label="Street", \
                              widget=forms.TextInput(attrs={\
                                'autocomplete':'off', \
                                'placeholder':'street', \
                                'tabindex':'15', \
                                'id':'addrstr', \
                                'title':'Street where you live'}))
    addrhousenum = forms.CharField(required=False, \
                                   label="House number", \
                                   widget=forms.TextInput(attrs={\
                                     'autocomplete':'off', \
                                     'placeholder':'house number', \
                                     'tabindex':'16', \
                                     'id':'addrhousenum', \
                                     'title':'Number of the house you live'}))
    addrapt = forms.CharField(required=False, \
                              label="Apartments", \
                              widget=forms.TextInput(attrs={\
                                'autocomplete':'off', \
                                'placeholder':'apartments', \
                                'tabindex':'17', \
                                'id':'addrapt', \
                                'title':'Your apartments\' number'}))
    addradditional = forms.CharField(required=False, \
                                     label="Address Addition", \
                                  widget=forms.TextInput(attrs={\
                                    'autocomplete':'off', \
                                    'placeholder':'addition', \
                                    'tabindex':'18', \
                                    'id':'addardditional', \
                                    'title':'Addition to your address'}))
    captcha = CaptchaField(label="You know what to do* ")
    
    def is_valid(self):
        
        is_valid = super(CreateUserForm, self).is_valid()
        if not is_valid:
            return is_valid
        
        #password match retypepassword
        
        if self.cleaned_data['password'] != self.cleaned_data['retypepassword']:
            err_msg = u'"password" and "retypepassword" must match'
            self.add_error("retypepassword", err_msg)                                                        
            is_valid = False
#            return False
        
        #email is already registered
            
        try:
            user = User.objects.get(email = self.cleaned_data['email'])
            if user:
                err_msg = u'This email is already registered in our system!'
                self.add_error("email", err_msg)
                is_valid = False
#                return False
        except User.DoesNotExist:
            pass
        
        #family exists
        
        if self.cleaned_data['family_email'] != "":
            if self.cleaned_data['family_email'] != self.cleaned_data['email']:
                try:
                    family = Family.objects.get(founder = \
                                          self.cleaned_data['family_email'])
                except Family.DoesNotExist:
                    err_msg = u'This family does not exist in our system!'
                    self.add_error("family_email", err_msg)
#                    return False
                    is_valid = False
        #birth date is valid
        
        if self.cleaned_data['birthdate'] !='':
            try:
                bdate = parse(self.cleaned_data['birthdate'])
                #age > 120 years
                max_age = relativedelta(years = 120)
                if bdate<datetime.now() - max_age:
                    err_msg = u'Age is more than 120 years'
                    self.add_error("birthdate", err_msg)
                    is_valid = False 
            except ValueError:
                err_msg = u'Birth date is incorrect'
                self.add_error("birthdate", err_msg)
                is_valid = False
#                return False
                
        
#                return False
        
        return is_valid
    
    def add_error(self, field, err_msg):
        try: 
            self._errors[field] = self._errors[field] + ErrorList([err_msg])
        except KeyError:
            self._errors[field] = ErrorList([err_msg])