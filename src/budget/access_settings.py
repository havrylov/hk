'''
Created on May 28, 2015

@author: thavr
'''
from audit.service import audit_event
from audit.models import AccessDataChange, AuditEventTypes
from budget.general import is_password_correct, send_email, return_full_name, \
    generate_confirmation, get_hostname
from budget.email_messages import get_body_email_conf, get_body_family_conf
from budget.debug import get_debug_user
from django.utils import timezone
from django.http import HttpResponse, HttpResponseForbidden, \
    HttpResponseServerError
from budget.forms.form_edit_access import EditAccess
from django.contrib.auth.decorators import login_required



def get_count_of_wrong_passwords_today(user):
    today_begin = timezone.now().replace(hour=0,minute=0,second=0,microsecond=0)
    try:
        entries = AccessDataChange.objects.filter(user = user).\
        filter(change_date__gte = today_begin)
    except:
        return -4
    return len(entries)

def parse_request(request):
    param_dictionary = {}
    try:
        param_dictionary['new_email'] = request.POST['new_email']
    except KeyError:
        param_dictionary['new_email'] = ''
    param_dictionary['new_password'] = request.POST.get(['new_password'], '')
    param_dictionary['retype_new_password'] = \
            request.POST.get(['retype_new_password'], '')
    param_dictionary['conf_password'] = request.POST.get(['conf_password'], '')
    return param_dictionary

def is_attempt_allowed(user):
    if get_count_of_wrong_passwords_today(user) >= 4:
        return False
    else:
        return True 

def save_access_data(user, new_parameters):
    acc_user = user.user    
    if new_parameters['new_email'] != '':
        acc_user.username = new_parameters['new_email']
        acc_user.email = new_parameters['new_email']
    if new_parameters['new_password'] != '':
        acc_user.set_password(new_parameters['new_password'])
    acc_user.save()
    user.emailisconfirmed = False
    user.save()    
    
def send_email_confirmation(user, host=''):
    code_conf = generate_email_confirmation(user)
    if (code_conf == -1) or (code_conf == -2):
        raise Exception
    #TODO: Here is just an excellent place for refactoring!!!            
    new_user_name = return_full_name(user.user.email, "New User")
    url = create_url(host, user.user.email, code_conf)
    body_email_conf = get_body_email_conf(new_user_name, user.user.email, url)
#DEUBG            
    user.addradditional = url
    user.save()
    subject_user_conf = "Email confirmation"
    send_email("we@housholdkeeper.com", user.user.email, subject_user_conf, \
                       body_email_conf)
          
    
    
def generate_email_confirmation(user):
    result = generate_confirmation(user, "email")
    return result

def create_url(host, email, code_conf, path="/budget/confirm" ):
    url = "http://"+host + path + "?email="+email+"&code="+code_conf
    return url      
    
def server_error(e, request):
    return HttpResponseServerError(str(request))

@login_required(login_url="/login/")
def change_access_data(request):
    #DEBUG section
    user = get_debug_user(request)    
    #DEBUG section
    attempt_audit = AccessDataChange(user_impacted = user, \
                    pasword_change= False, \
                    email_change= False, \
                    change_date = timezone.now(), \
                    password_verification_result = 'Pending')
    try:
        request_parameters = parse_request(request)
    except Exception as e:
        return server_error(e, request)
    if request_parameters['new_email'] != '':
        attempt_audit.email_change = True
    if request_parameters['new_password'] != \
                                    request_parameters['retype_new_password']:
        return server_error(e, request)
    if request_parameters['new_password'] != '':
        attempt_audit.pasword_change = True
    try: 
        attempt_is_allowed = is_attempt_allowed(user)
    except Exception as e:
        return server_error(e, request)
    if not attempt_is_allowed:
        response = HttpResponse("OK.", content_type="text/plain")
        response['Overflow'] = "1" 
        attempt_audit.password_verification_result = 'Fail'
        try:
            attempt_audit.save()
        except Exception as e:
            return server_error(e, request)
        return response
    try:
        password_is_correct = is_password_correct(user, \
                                request_parameters["conf_password"])
    except Exception as e:
        return server_error(e, request)
    if not password_is_correct:
        response = HttpResponse("OK.", content_type="text/plain")
        response['Overflow'] = "-6" 
        attempt_audit.password_verification_result = 'Fail'
        try:
            attempt_audit.save()
        except Exception as e:
            return server_error(e, request)
        return response
    try:
        save_access_data(user, request_parameters)
    except Exception as e:
        return server_error(e, request)                
    response = HttpResponse("OK.", content_type="text/plain")
    response['Overflow'] = "0" 
    attempt_audit.password_verification_result = 'Success'    
    try:
        attempt_audit.save()
    except Exception as e:
        return server_error(e, request)
    try:
        send_email_confirmation(user, get_hostname(request))
    except Exception as e:
        return server_error(e, request)
    audit_created = audit_event(user, user,\
                                        AuditEventTypes.user_edited())
    if not audit_created:
        return HttpResponseServerError("NOK")
    return response    

@login_required(login_url="/login/")
def user_access_edit_form_validation(request):
    if request.method == 'POST':
        edit_user_access_form = EditAccess(request.POST)
        if edit_user_access_form.is_valid(): 
            response = change_access_data(request)
            return response
    else:
        edit_user_access_form = EditAccess() # An unbound form
    return server_error(None, request)
    #return access_data(request, user, user_form=edit_user_access_form)