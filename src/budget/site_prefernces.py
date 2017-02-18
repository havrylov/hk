'''
Created on Mar 22, 2016

@author: thavr
'''
from budget.debug import get_debug_user
from budget.views import site_preferences, failure_page
from django.contrib.auth.decorators import login_required
from budget.forms.form_edit_prefernces import EditPreferncesForm
from django.http import HttpResponse, HttpResponseForbidden, \
    HttpResponseServerError
from budget.models import UserSettings, SitePreferncesList, SitePrefernce, \
                          Currency
from audit.service import audit_event
from audit.models import AuditEventTypes

@login_required(login_url="/login/")
def preferences(request):
    #<DEBUG SECTION>    
    user = get_debug_user(request)
    #<DEBUG SECTION>
    return site_preferences(request, user)

@login_required(login_url="/login/")
def user_edit_site_prefernces_form_validation(request):
    if request.method == 'POST':
        edit_site_preferences_form = EditPreferncesForm(request.POST)
        if edit_site_preferences_form.is_valid(): 
            response = change_site_prefernces(request)
            return response
    else:
        edit_user_access_form = EditPreferncesForm() # An unbound form
    return server_error(None, request)

def server_error(e, request):
    return HttpResponseServerError(str(request))

@login_required(login_url="/login/")
def change_site_prefernces(request):    
    #DEBUG section
    user = get_debug_user(request)    
    #DEBUG section    
    try:
        request_parameters = parse_request(request)
    except Exception as e:
        return server_error(e, request)
    current_preferences = user.get_settings_with_name()
    prefernces_name_value = user.get_user_settings_as_voc()
    for sett_name, new_value in request_parameters.iteritems():
        entry_exists = True
        audit_list = []
        new_bool = None
        new_float = None
        new_string = None        
        try:
            old_preference = current_preferences[sett_name]
        except KeyError as e:
            recreate_setting = SitePreferncesList.objects.get(setting_name\
                                                     =sett_name)
            setting_conn = SitePrefernce.objects.get(setting =recreate_setting)
            if setting_conn.type.prefernce_type == 'bool':
                new_bool = request_parameters[sett_name]                
            elif setting_conn.type.prefernce_type == 'float':
                new_float = request_parameters[sett_name]
            elif setting_conn.type.prefernce_type == 'string':
                new_string = request_parameters[sett_name]
            elif setting_conn.type.prefernce_type == 'int':
                new_int = request_parameters[sett_name]
            users_default_settings = UserSettings(user = user, \
                                                  setting = setting_conn, \
                                                  value_bool = new_bool, \
                                                  value_float = new_float, \
                                                  value_int = new_int, \
                                                  value_string = new_string)
            users_default_settings.save()            
            change_dic = {"field": sett_name, "old_value": None, \
                      "new_value": request_parameters[sett_name]}
            audit_list.append(change_dic)
            entry_exists = False
        
        if entry_exists and prefernces_name_value[sett_name] != \
                                        request_parameters[sett_name]:
            setting_type = \
                    current_preferences[sett_name].setting.type.prefernce_type
            if setting_type == 'bool':
                new_bool = new_value                
            elif setting_type == 'float':
                new_float = new_value
            elif setting_type == 'string':
                new_string = new_value
            elif setting_type == 'int':
                new_int = new_value
            old_preference.value_bool = new_bool
            old_preference.value_float = new_float
            old_preference.value_string = new_string
            old_preference.value_int = new_int            
            try:
                old_preference.save()
            except:            
                return failure_page(request, "Failed on user saving<br>")
            change_dic = {"field": sett_name, \
                    "old_value": prefernces_name_value[sett_name], \
                    "new_value": request_parameters[sett_name]}
            audit_list.append(change_dic)
            audit_created = audit_event(user, user,\
                                    AuditEventTypes.site_preferences_edited(), \
                                    list_of_changes = audit_list)
            if not audit_created:
                raise Exception        
    response = HttpResponse("OK.", content_type="text/plain")
    response['Overflow'] = "0"
    return response    
    
        #TODO: Implement successfl output
    
#     attempt_audit = AccessDataChange(user_impacted = user, \
#                     pasword_change= False, \
#                     email_change= False, \
#                     change_date = timezone.now(), \
#                     password_verification_result = 'Pending')
#     try:
#         request_parameters = parse_request(request)
#     except Exception as e:
#         return server_error(e, request)
#     if request_parameters['new_email'] != '':
#         attempt_audit.email_change = True
#     if request_parameters['new_password'] != \
#                                     request_parameters['retype_new_password']:
#         return server_error(e, request)
#     if request_parameters['new_password'] != '':
#         attempt_audit.pasword_change = True
#     try: 
#         attempt_is_allowed = is_attempt_allowed(user)
#     except Exception as e:
#         return server_error(e, request)
#     if not attempt_is_allowed:
#         response = HttpResponse("OK.", content_type="text/plain")
#         response['Overflow'] = "1" 
#         attempt_audit.password_verification_result = 'Fail'
#         try:
#             attempt_audit.save()
#         except Exception as e:
#             return server_error(e, request)
#         return response
#     try:
#         password_is_correct = is_password_correct(user, \
#                                 request_parameters["conf_password"])
#     except Exception as e:
#         return server_error(e, request)
#     if not password_is_correct:
#         response = HttpResponse("OK.", content_type="text/plain")
#         response['Overflow'] = "-6" 
#         attempt_audit.password_verification_result = 'Fail'
#         try:
#             attempt_audit.save()
#         except Exception as e:
#             return server_error(e, request)
#         return response
#     try:
#         save_access_data(user, request_parameters)
#     except Exception as e:
#         return server_error(e, request)                
#     response = HttpResponse("OK.", content_type="text/plain")
#     response['Overflow'] = "0" 
#     attempt_audit.password_verification_result = 'Success'    
#     try:
#         attempt_audit.save()
#     except Exception as e:
#         return server_error(e, request)
#     try:
#         send_email_confirmation(user, get_hostname(request))
#     except Exception as e:
#         return server_error(e, request)
#     audit_created = audit_event(user, user,\
#                                         AuditEventTypes.user_edited())
#     if not audit_created:
#         return HttpResponseServerError("NOK")
#     return response


def parse_request(request):
    param_dictionary = {}
    try:
        default_tab = request.POST['start_tab']         
    except KeyError as e:
        default_tab = 'pub'        
    if default_tab == 'pub':
        param_dictionary['default_tab_is_public'] = True
    elif default_tab == 'priv':
        param_dictionary['default_tab_is_public'] = False
    else:
        raise KeyError(e)
    try:
        currency_mark = request.POST['curr']
    except KeyError as e:
        currency_mark = "GUC"
    param_dictionary['main_currency'] = \
                        Currency.objects.get(short_name = currency_mark).pk
    return param_dictionary