'''
Created on Sep 25, 2015

@author: thavr
'''
from test_data.forms.form_create_test_users import CreateTestUsersForm
import django


django.setup()
data={'users':'123', 'min_transactions':"2", 'max_transactions':'1'}
f = CreateTestUsersForm(data)
result = f.is_valid()
print f.errors