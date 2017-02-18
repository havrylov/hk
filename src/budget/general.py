'''
Created on Jun 15, 2014

@author: thavr
'''

# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from budget.models import ConfirmationData, Users
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from django.http import HttpResponse, HttpResponseForbidden, \
HttpResponseServerError
from budget.debug import get_debug_user
from django.contrib.auth.hashers import check_password 

def send_email(sender, reciever, subject, body):
    return True

def return_full_name(email, default_name):
    full_name = User.objects.get_by_natural_key(email).get_full_name()
    if full_name == "":
        full_name = default_name
    return full_name

def generate_confirmation_string():
    from hashlib import md5, sha512
    from random import seed, randint
    seed()
    rawString = ""
    for i in range(35):
        rawString += chr(randint(32,127))
    encodedString = md5(sha512(rawString.encode()).hexdigest()\
                        .encode()).hexdigest()
    return encodedString

def generate_confirmation(user, conf_type):
    if conf_type == "email":
        conf_type = ConfirmationData.confirmation_email
        expires_in_days = 30
    elif conf_type == "family":
        conf_type = ConfirmationData.confirmation_family
        expires_in_days = 30
    elif conf_type == "password":
        conf_type = ConfirmationData.confirmation_password
        expires_in_days = 30
    elif conf_type == "delete":
        conf_type = ConfirmationData.confirmation_delete
        expires_in_days = 30
    else:
        return -1 #Wrong Input data. No confirmation type was found
    
    code = generate_confirmation_string()
    
    today = timezone.now()
    
    expires_at = today + relativedelta(days=expires_in_days)
    
    try:
        confirmation = ConfirmationData(user = user, sentat = timezone.now(),\
                                    code = code, type = conf_type, \
                                    is_expired=False, \
                                    expiratin_date = expires_at)
        confirmation.save()
    except Exception as e:
        return -2 #DB communication error
    return code #OK
            
    
def get_real_user(request):
    uu = request.user
    user = Users.objects.get(user=uu)
    
    return user  

def is_float(value):
    try:
        a = float(value)
    except ValueError:
        return False
    return True

def is_date(value):
    try:
        a = parse(value)
    except ValueError:
        return False
    return True

def get_hostname(request):
    try:
        hostname = request.get_host()
    except:
        hostname = "xxx.com"
        
    return hostname

def is_password_correct(user, plain_password):
    encoded_password = user.user.password
    if check_password(plain_password, encoded_password):
        return True
    else:
        return False