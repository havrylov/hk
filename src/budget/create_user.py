'''
Created on May 16, 2014

@author: thavr
'''

from budget.models import Users, Family, Pseudonym, UserSettings, \
    SitePreferncesList, SitePrefernce
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from budget.views import failure_page, register_success, register
from dateutil.parser import parse
from budget.general import send_email, return_full_name, generate_confirmation,\
    get_hostname
from budget.email_messages import get_body_email_conf, get_body_family_conf
from audit.service import audit_event
from audit.models import AuditEventTypes
from budget.forms.form_create_user import CreateUserForm

# Entry point - parse_inputs()
# Outputs:
#     [family, User, Users, is_family_new] - successful execution
#     -1: Program failure by creating User in auth
#     -2: Program failure by creating User in budget
#     -3: 

def user_creation_procedure(request, parameters=False):
    if not parameters:
        user_parameters=parse_inputs(request)
    else:
        user_parameters = parameters
    if user_parameters == -1:
        return failure_page(request ,"Failed on parsing")
    # TODO: redirect to registration pages
    hostname = get_hostname(request)
    general_result = create_user_logic(user_parameters['email'], \
                                       user_parameters['password'], \
                                       user_parameters, \
                                       hostname)
#     general_result =[1,2]
    temp_val = 0 
    try:
        temp_val = len(general_result)
    except TypeError:
        pass
#        return failure_seite(request)
    if temp_val == 4:
        response = register_success(request, general_result)
        return response
    else:
        return failure_page(request, \
                             "Failed on user creation<br>"+str(general_result))
        
def user_creation_procedure_with_form(request):
    if request.method == 'POST':
        create_user_form = CreateUserForm(request.POST)
        if create_user_form.is_valid(): 
            response = user_creation_procedure(request)
            return response
    else:
        create_user_form = CreateUserForm() # An unbound form

    return register(request, user_form=create_user_form)
        

def parse_inputs(request):
    # Convert POST request parameters to dictionary
    
    optional_parameters = {'birthdate':'birthdate','cellcountry':'cellcountry',\
                           'cellarea':'cellarea', 'cellnum':'cellnumber', \
                           'addrcountry':'addrcountry', \
                           'addrpostid':'addrpostid', 'addrtown':'addrcity', \
                           'addrstr':'addrstr','addrhousenum':'addrhousenum',\
                           'addrapt':'addrapt', 'fname':'fname', \
                           'addradditional':'addradditional','sname':'sname', \
                           'family_email':'family_email'}
    param_dictionary = {}
    try:
        param_dictionary['email'] = request.POST['email']
        param_dictionary['password'] = request.POST['password']
#        param_dictionary['family_email'] = request.POST['family_email']
        
        for name, param in optional_parameters.iteritems():
            val = check_post_param(request, param)
            param_dictionary[name] = val
        
        if param_dictionary['birthdate'] == '':
            param_dictionary['birthdate'] = None
        else:
            param_dictionary['birthdate'] = \
                    parse(param_dictionary['birthdate']).strftime("%Y-%m-%d")
        
#         param_dictionary['cellcountry'] = request.POST['cellcountry']
#         param_dictionary['cellarea'] = request.POST['cellarea']
#         param_dictionary['cellnum'] = request.POST['cellnumber']
#         param_dictionary['addrcountry'] = request.POST['addrcountry']
#         param_dictionary['addrpostid'] = request.POST['addrpostid']
#         param_dictionary['addrtown'] = request.POST['addrcity']
#         param_dictionary['addrstr'] = request.POST['addrstr']
#         param_dictionary['addrhousenum'] = request.POST['addrhousenum']
#         param_dictionary['addrapt'] = request.POST['addrapt']
#         param_dictionary['addradditional'] = request.POST['addradditional']
#         param_dictionary['fname'] = request.POST['fname']
#         param_dictionary['sname'] = request.POST['sname']
    except KeyError:
        return -1 
    except ValueError:
        return -1
    return param_dictionary

def check_post_param(request, param_name):
    
    try:
        output_value = request.POST[param_name]
    except KeyError:
        output_value = ''
    
    return output_value

    

def email_already_registered(email_address):
    try:
        temp_user = User.objects.get(email=email_address)
        return True
    except ObjectDoesNotExist:
        return False
    except Exception as e:
        return -1
    
def family_exist(email_address):
    # Output:
    #  Family : if family is found
    #   False : if family is not found
    #   0 : If error took place during execution 
    try:
        temp_family = Family.objects.get(founder=email_address)
        return temp_family
    except ObjectDoesNotExist:
        return False
    except:
        return 0
    
def create_family(email):
    # Output:
    #  False : the family creation was not successful
    #  family: created family
    if not family_exist(email):        
        try:
            new_family = Family(founder=email)
            new_family.save()
        except Exception:            
            return False
    else:
        return False
     
    return new_family
 
 
    
def create_user_logic(email, password, other_params, host):

    if email_already_registered(email):
        return -5  # The email already exists in DB. Password recover?

# Analyzing family-user email presence/registration     


    if other_params["family_email"] == '' and family_exist(email):
        return -6  # Email is not registered however the family exists
        
    if (other_params["family_email"] == '')\
    or \
    (other_params["family_email"] == email):
        new_family = create_family(email)
        if new_family:
            new_users = create_user(email, password, new_family, \
                                    other_params , family_confirmed='True', \
                                    host=host)
            try:
                temp_val = len(new_users)
            except:
                
                new_family.delete()
                return new_users  # Error by creating new user
        else:
            return -2  # Error by creating new family  
        
        return_value = [new_family]
        for user_realted in new_users:
            return_value.append(user_realted)
        return_value.append(True)    
        return return_value
    
    if family_exist(other_params['family_email']) \
    and \
    other_params['family_email'] != email:
        old_family = family_exist(other_params['family_email'])
        if old_family:
            new_users = create_user(email, other_params['password'], \
                                    old_family, other_params, \
                                    family_confirmed=False, host=host)
            
            try:
                temp_val = len(new_users)
            except:
                return new_users  # Error by creating new user
            family_pseudos = create_pseudonyms_for_all(new_users[1])
            if not family_pseudos:
                new_users[1].delete()
                new_users[0].delete()
                return -4
        else:
            return -3  # Error by finding family that already exists
        return_value = [old_family]
        for user_realted in new_users:
            return_value.append(user_realted)
        return_value.append(False)        
        return return_value
        
def create_user(email, password, family, other_params, family_confirmed=False, \
                host=""):
    # Output:
    #     -1 : user in auth is not created
    #     -2 : user in Users is not created
    #     -3 : the inputs are wrong
    if verify_inputs(email, password, family, other_params, family_confirmed):
        try:
            user = User.objects.create_user(username=email, \
                                            email=email, \
                                            password=password, \
                                            first_name=other_params['fname'], \
                                            last_name=other_params['sname'])
            user_from_users = Users(user=user, \
                                    family=family, \
                                    emailisconfirmed=False, \
                                    birthdate=other_params['birthdate'], \
                                    regdate=timezone.now(), \
                                    famidconfirmed=family_confirmed, \
                                    cellcountry=other_params['cellcountry'], \
                                    cellarea=other_params['cellarea'], \
                                    cellnum=other_params['cellnum'], \
                                    addrcountry=other_params['addrcountry'], \
                                    addrpostid=other_params['addrpostid'], \
                                    addrtown=other_params['addrtown'], \
                                    addrstr=other_params['addrstr'], \
                                    addrhousenum=other_params['addrhousenum'], \
                                    addrapt=other_params['addrapt'], \
                                    addradditional=other_params['addradditional'])
            user_from_users.save()
            def_tab = SitePreferncesList.objects.get(setting_name\
                                                     ="default_tab_is_public")
            setting_conn = SitePrefernce.objects.get(setting =def_tab)
            users_default_settings = UserSettings(user = user_from_users, \
                                                  setting = setting_conn, \
                                                  value_bool = True)
            users_default_settings.save()
            code_conf = generate_email_confirmation(user_from_users)
            if (code_conf == -1) or (code_conf == -2):
                raise Exception
#TODO: Here is just an excellent place for refactoring!!!            
            new_user_name = return_full_name(email, "New User")
            url = create_url(host, email, code_conf)
            body_email_conf = get_body_email_conf(new_user_name, email, url)
#DEUBG            
            user_from_users.addradditional = url
            user_from_users.save()
            subject_user_conf = "Email confirmation"
            send_email("we@housholdkeeper.com", email, subject_user_conf, \
                       body_email_conf)
            
            if not family_confirmed:
                code_family_conf = generate_email_confirmation(user_from_users)
                if (code_family_conf == -1) or (code_family_conf == -2):
                    raise Exception            
                family_founder_name = return_full_name(family.founder, \
                                                       "Family founder")
                url = create_url(host, email, code_conf)
                body_family_conf = get_body_family_conf(family_founder_name, \
                                                        email, url)
                subject_family_conf = "New member wants to join your family"
                send_email("we@householdkeeper.com", family.founder, \
                           subject_family_conf, body_family_conf)
                user_from_users.addradditional = url
                user_from_users.save()
            audit_created = audit_event(user_from_users, user_from_users,\
                                        AuditEventTypes.user_created())
            if not audit_created:
                raise Exception
            
        except Exception as e:
            try:
                user.delete()
            except:
                pass
            return -399
        return [user, user_from_users]
    else:
        return -3
    
def generate_email_confirmation(user):
    result = generate_confirmation(user, "email")
    return result
    
def generate_family_confirmation(user):
    result = generate_confirmation(user, "family")
    return result
    
def create_url(host, email, code_conf, path="/budget/confirm" ):
    url = "http://"+host + path + "?email="+email+"&code="+code_conf
    return url

def create_pseudonyms_for_all(new_user):
    for family_member in Users.objects.filter(family = new_user.family):
        if family_member != new_user:
            try: 
                new_pseudo_for = Pseudonym(pseudonym = "", \
                                           of_the_user = family_member, \
                                           for_the_user = new_user)
                new_pseudo_of = Pseudonym(pseudonym = "", \
                                           for_the_user = family_member, \
                                           of_the_user = new_user)
                new_pseudo_for.save()
                new_pseudo_of.save()
            except:
                return -1
    return True
        
        
        
        
def verify_inputs(email, password, family, kwargs, family_confirmed):
    return True
