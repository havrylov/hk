'''
Created on Sep 24, 2015

@author: thavr
'''

from django import forms
from django.forms.utils import ErrorList

class CreateTestUsersForm(forms.Form):
    users = forms.IntegerField(required=True, \
                            label="Number of Test Users:", \
                            max_value = 250000, min_value=1)
    min_transactions = forms.IntegerField(required=True, \
                            label="Minimal number of transactions per user:", \
                            min_value=1)
    max_transactions = forms.IntegerField(required=True, \
                            label="Maximal number of transactions per user:", \
                            min_value=1)
    
    def is_valid(self):
        
        is_valid = super(CreateTestUsersForm, self).is_valid()
        if not is_valid:
            return is_valid
        
        try:
            gen_users = int(self.cleaned_data['users'])
            if gen_users <=0:
                self.add_error("usersmustbepos", \
                               "Number of users must be bigger than 0!")
                is_valid = False
        except ValueError:
            self.add_error("usersmustbeint", "Number of users must be integer!")
            is_valid = False
            
        try:
            min_trans = int(self.cleaned_data['min_transactions'])
            if min_trans <=0:
                self.add_error("min_transactionsmustbepos", \
                       "Minimal number of transaction must be bigger than 0!")
                is_valid = False
        except ValueError:
            self.add_error("min_transactionsmustbeint", \
                           "Minimal number of transaction must be integer!")
            is_valid = False
            
            
        try:
            max_trans = int(self.cleaned_data['max_transactions'])
            if max_trans <=0:
                self.add_error("max_transactionsmustbepos", \
                       "Maximal number of transaction must be bigger than 0!")
                is_valid = False
        except ValueError:
            self.add_error("max_transactionsmustbeint", \
                       "Maximal number of transaction must be integer!")
            is_valid = False
            
        try:
            max_trans = int(self.cleaned_data['max_transactions'])
            min_trans = int(self.cleaned_data['min_transactions'])
            if max_trans < min_trans:
                self.add_error("max_transactionsmustbemore", \
                   "Maximal number of transaction must be bigger than minimal!")
                is_valid = False
        except ValueError:
            pass
            
        return is_valid
    
    def add_error(self, field, err_msg):
        try: 
            self._errors[field] = self._errors[field] + ErrorList([err_msg])
        except KeyError:
            self._errors[field] = ErrorList([err_msg])
            
        