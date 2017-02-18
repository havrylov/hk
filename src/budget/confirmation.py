'''
Created on Jun 26, 2014

@author: thavr
'''

from budget.views import failure_page, confirmation_success,\
    confirmation_resent_success, no_more_confirmations_today
from budget.models import ConfirmationData, Users
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from budget.debug import get_debug_user
from datetime import datetime
from budget.create_user import generate_email_confirmation, create_url
from budget.general import return_full_name, get_hostname, send_email
from budget.email_messages import get_body_email_conf, get_body_family_conf
from audit.service import audit_event
from audit.models import AuditEventTypes
from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth.decorators import login_required

def confirmation_procdedure(request):
    conf_parameters = parse_request(request)
    if conf_parameters == -1:
        return failure_page(request ,"Failed on parsing")
    conf_entry = get_confirmation_entry(conf_parameters)
    if conf_entry == -4:
        return failure_page(request ,"Incorrect parameters<br>"+\
                             conf_parameters)
    some_inter_result = check_expiration(conf_entry)
    if some_inter_result == -6:
        return failure_page(request ,"Failed to save changes to confirmation")
    if conf_entry.is_expired or conf_entry.expiratin_date < timezone.now():
        return failure_page(request, "Code is expired")
    if not conf_entry.is_active:
        return failure_page(request, "The code was already used")
    
    final_result = execute_confirmation(conf_entry)
    if final_result==-7:
        return failure_page(request, "Failed saving of the emailisconfirmed")
    elif final_result==-8:
        return failure_page(request, "Failed saving of the famidconfirmed")
    elif final_result==-9:
        return failure_page(request, "Failed saving of the is_active")
    
    return confirmation_success(request)

    
def execute_confirmation(conf_entry):
    user = conf_entry.user
    if conf_entry.type == ConfirmationData.confirmation_email:
        user.emailisconfirmed = True
        try:
            user.save()
        except:
            return -7
        #TODO: Here should be implemented mechanism to send family confirmation email after email is confirmed
        # and user is not founder of the family
    elif conf_entry.type == ConfirmationData.confirmation_family:
        user.famidconfirmed = True
        try:
            user.save()
        except:
            return -8
    conf_entry.is_active = False
    try:
        conf_entry.save()
    except:
        return -9
    return 0
    
    
def check_expiration(entry_to_check):
    if entry_to_check.is_active:
        if entry_to_check.expiratin_date < timezone.now():
            entry_to_check.is_expired = True
            #Define Audit event type
            if entry_to_check.type == "email":
                event_type = AuditEventTypes.email_confirmation_expired()
            elif entry_to_check.type == "family":
                event_type = AuditEventTypes.email_confirmation_expired()
            else:
                event_type = AuditEventTypes.unknown_event()
            try:
                entry_to_check.save()
                audit_event(entry_to_check.user, entry_to_check.user, \
                        event_type, confirmation=entry_to_check)
            except:
                return -6
    return 0
        
    
    
def get_confirmation_entry(conf_param):
    email_user = conf_param['email']
    code_user = conf_param['code']
    user_candidate = get_user_data(email_user)
    try:
        result_entry = ConfirmationData.objects.filter(user = user_candidate).\
                                                        get(code = code_user)
    except:
        return -4
    return result_entry
        
def get_user_data(email):
    try:
        auth_user = get_object_or_404(User, email = email)
    except:
        return -2
    try:
        user = Users.objects.get(user = auth_user)
    except:
        return -3
    return user

    
def parse_request(request):
    param_dictionary = {}
    try:
        param_dictionary['email'] = request.GET['email']
        param_dictionary['code'] = request.GET['code']
    except KeyError:
        return -5 
    return param_dictionary

def get_count_confirmations_today(user):
    today_begin = timezone.now().replace(hour=0,minute=0,second=0,microsecond=0)
    try:
        entries = ConfirmationData.objects.filter(user = user).\
        filter(sentat__gte = today_begin)
    except:
        return -4
    return len(entries)

@login_required(login_url="/login/")
def resend_confirmation(request, type = "email"):
    #DEBUG section
    user = get_debug_user(request)    
    #DEBUG section
    if get_count_confirmations_today(user) > 2:
        return -6
    code_conf = generate_email_confirmation(user)
    if (code_conf == -1) or (code_conf == -2):
        return -7
#TODO: Here is just an excellent place for refactoring!!!          
    
    
    host = get_hostname(request)
    url = create_url(host, user.user.email, code_conf)
    if type == "email":
        receiver = user.user.email
        subject = "Household keeper: Email confirmation"
        new_user_name = return_full_name(receiver, "New User")
        body_email = get_body_email_conf(new_user_name, \
                                              receiver, url)
    elif type == "family":
        receiver = user.family.founder
        family_founder_name = return_full_name(receiver, \
                                                       "Family founder")                
        body_email = get_body_family_conf(family_founder_name, \
                                                        user.user.email, url)
        subject = "Household keeper: New member wants to join your family"
    else:
        return -8
    email_is_sent = send_email("we@householdkeeper.com", receiver, subject, \
               body_email)
    if not email_is_sent:
        return -9
    return 1

def resend_family_confirmation(request):
    result = resend_confirmation(request, "family")
    if result == 1:
        response = HttpResponse("OK.", content_type="text/plain")
        response['Overflow'] = "1"        
    elif result == -6:
        response = HttpResponse("NOK.", content_type="text/plain")
        response['Overflow'] = "-6"  
    else:
        response = HttpResponseServerError("NOK.", content_type="text/plain")
    return response
    
def resend_email_confirmation(request):
    result = resend_confirmation(request, "email")
    if result == 1:
        response = HttpResponse("OK", content_type="text/plain")
        response['Overflow'] = 1        
    elif result == -6:
        response = HttpResponse("NOK", content_type="text/plain")
        response['Overflow'] = -6  
    else:
        response = HttpResponseServerError("NOK.", content_type="text/plain")
    return response