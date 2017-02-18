'''
Created on Jun 30, 2014

@author: thavr
'''

from budget.views import login
from budget import views
from django.shortcuts import redirect
from budget.debug import get_debug_user
from django.contrib.auth import logout

def login(request):
    return login(request)

def logout_user(request):
    logout(request)
    return views.logout(request)

def signin(request):
    return redirect("test_data:test_users")

