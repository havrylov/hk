'''
Created on Oct 28, 2014

@author: thavr
'''
from django import forms

class EditAccess(forms.Form):    
    new_email = forms.EmailField(label="New Email Address ", \
                             widget=forms.EmailInput(attrs={\
                                 'autocomplete':'off', \
                                 'placeholder':'email', \
                                 'tabindex':'2', \
                                 'id':'new_email', \
                                 'title':'New email address'}))       
#     old_password = forms.CharField(label="Old Password ", \
#                                widget = forms.PasswordInput(attrs={\
#                                  'autocomplete':'off', \
#                                  'placeholder':'old password', \
#                                  'tabindex':'3', \
#                                  'id':'password', \
#                                  'title':'Type your current password'}))
    new_password = forms.CharField(label="New Password ", \
                               widget = forms.PasswordInput(attrs={\
                                 'autocomplete':'off', \
                                 'placeholder':'new password', \
                                 'tabindex':'4', \
                                 'id':'password', \
                                 'title':'Type new desirable password here'}))
    
    retype_new_password = forms.CharField(label="Retype New Password ", \
                                     widget = forms.PasswordInput(attrs={\
                                     'autocomplete':'off', \
                                     'placeholder':'retype new password', \
                                     'tabindex':'5', \
                                     'id':'retypepassword', \
                                     'title':'Retype your new desirable' + \
                                     ' password'}))