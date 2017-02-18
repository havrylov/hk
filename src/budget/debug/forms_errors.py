'''
Created on Aug 21, 2014

@author: thavr
'''
from budget.forms.form_create_user import CreateUserForm
import django

django.setup()
data={'email':'123@qwweq.qq', 'password':"1", 'retypepassword':'2', \
      'birthdate':'1.1.1987'}
f = CreateUserForm(data)
result = f.is_valid()
print f.errors