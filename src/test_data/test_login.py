'''
Created on Oct 12, 2015

@author: thavr
'''
from django.shortcuts import redirect
from budget.models import Users
from django.contrib.auth import login, authenticate

def login_test_user(request, id=0):
    try:
        if id == 0:
            user_id = int(request.GET["id"])
        else:
            user_id = id
        user = Users.objects.get(pk=user_id)
    except Exception as e:
        redirect ("test_data:test_users")
    uu = authenticate(username=user.user.username, password="12345678")
    login(request, uu)
    return redirect("budget:main")
        