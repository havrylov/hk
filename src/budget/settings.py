'''
Created on Jul 7, 2014

@author: thavr
'''

from budget.debug import get_debug_user
from budget.views import personal_settings, failure_page, saved_success,\
    family_setings, edit_wo_form, access_data, site_preferences
from dateutil.parser import parse
from budget.models import User, Users, Pseudonym
from django.shortcuts import redirect
from audit.service import audit_event
from audit.models import AuditEventTypes
from budget.forms.form_edit_user import EditUserForm
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def personal(request):
    #<DEBUG SECTION>    
    user = get_debug_user(request)
    #<DEBUG SECTION>
    return personal_settings(request, user)
@login_required(login_url="/login/")
def access(request):
    #<DEBUG SECTION>    
    user = get_debug_user(request)
    #<DEBUG SECTION>
    return access_data(request, user)

@login_required(login_url="/login/")
def personal_forms(request):
    #<DEBUG SECTION>    
    user = get_debug_user(request)
    #<DEBUG SECTION>
    return edit_wo_form(request, user)

@login_required(login_url="/login/")
def family(request):
    #<DEBUG SECTION>    
    user = get_debug_user(request)
    #<DEBUG SECTION>
    if len(user.get_all_members()) <=1:
        return redirect("/main")
    return family_setings(request, user)

@login_required(login_url="/login/")
def save_family_pseudos(request):
    #<DEBUG SECTION>    
    for_user = get_debug_user(request)
    #<DEBUG SECTION>
    params_array = request_to_array(request)
    for entry in params_array:
        of_user = entry["user"]
        pseudonym = entry["pseudo"]
        try:
            new_pseudo = Pseudonym.objects.get(of_the_user = of_user, \
                                               for_the_user = for_user)
            new_pseudo.pseudonym = pseudonym
        except Pseudonym.DoesNotExist:
            new_pseudo = Pseudonym(pseudonym = pseudonym, \
                                   of_the_user = of_user, \
                                   for_the_user = for_user)
        try:
            new_pseudo.save()
        except:
            return failure_page(request)
    return  saved_success(request)
    
def request_to_array(request):
    outp = []
    index = 0
    for val in request.POST.getlist('user'):
        defined_user_auth = User.objects.get(email=val)
        defined_user = Users.objects.get(user=defined_user_auth)
        entry = {'user':defined_user, \
                 'pseudo':request.POST.getlist('pseudo')[index]}
        index = index + 1
        outp.append(entry)
    return outp 

@login_required(login_url="/login/")
def user_edit_form_validation(request):
    # <DEBUG SECTION>
    user = get_debug_user(request)
    # <DEBUG SECTION> 
    if request.method == 'POST':
        edit_user_form = EditUserForm(request.POST)
        if edit_user_form.is_valid(): 
            response = save_settings(request)
            return response
    else:
        edit_user_form = EditUserForm() # An unbound form

    return personal_settings(request, user, user_form=edit_user_form)       
    
@login_required(login_url="/login/")
def save_settings(request):
    # <DEBUG SECTION>
    user = get_debug_user(request)
    # <DEBUG SECTION>
    audit_list = []
    params = parse_inputs_personal(request)
    if params == -1:
        return failure_page(request, "Failed on parsing inputs<br>")
    
    if user.birthdate != params['birthdate']:
        change_dic = {"field": "birthdate", "old_value": user.birthdate, \
                      "new_value": params['birthdate']}
        audit_list.append(change_dic)
        user.birthdate = params['birthdate']
          
        
    if user.cellcountry != params['cellcountry']:
        change_dic = {"field": "cellcountry", "old_value": user.cellcountry, \
                      "new_value": params['cellcountry']}
        audit_list.append(change_dic)     
        user.cellcountry = params['cellcountry']
    
    if user.cellarea != params['cellarea']:   
        change_dic = {"field": "cellarea", "old_value": user.cellarea, \
                      "new_value": params['cellarea']}
        audit_list.append(change_dic)
        user.cellarea = params['cellarea']
        
    if user.cellnum != params['cellnum']:        
        change_dic = {"field": "cellnum", "old_value": user.cellnum, \
                      "new_value": params['cellnum']}
        audit_list.append(change_dic)
        user.cellnum = params['cellnum']
        
    if user.addrcountry != params['addrcountry']:
        change_dic = {"field": "addrcountry", "old_value": user.addrcountry, \
                      "new_value": params['addrcountry']}
        audit_list.append(change_dic)
        user.addrcountry = params['addrcountry']
        
    if user.addrpostid != params['addrpostid']:
        change_dic = {"field": "addrpostid", "old_value": user.addrpostid, \
                      "new_value": params['addrpostid']}
        audit_list.append(change_dic)
        user.addrpostid = params['addrpostid']
     
    if user.addrtown != params['addrtown']:   
        change_dic = {"field": "addrtown", "old_value": user.addrtown, \
                      "new_value": params['addrtown']}
        audit_list.append(change_dic)
        user.addrtown = params['addrtown']
        
    if user.addrstr != params['addrstr']:   
        change_dic = {"field": "addrstr", "old_value": user.addrstr, \
                      "new_value": params['addrstr']}
        audit_list.append(change_dic)
        user.addrstr = params['addrstr']
        
    if user.addrhousenum != params['addrhousenum']:
        change_dic = {"field": "addrhousenum", "old_value": user.addrhousenum, \
                      "new_value": params['addrhousenum']}
        audit_list.append(change_dic)
        user.addrhousenum = params['addrhousenum']
        
    if user.addrapt != params['addrapt']:
        change_dic = {"field": "addrapt", "old_value": user.addrapt, \
                      "new_value": params['addrapt']}
        audit_list.append(change_dic)
        user.addrapt = params['addrapt']
        
    if user.addradditional != params['addradditional']:
        change_dic = {"field": "addradditional", \
                      "old_value": user.addradditional, \
                      "new_value": params['addradditional']}
        audit_list.append(change_dic)
        user.addradditional = params['addradditional']
        
        
    user_auth = user.user
        
    if user_auth.first_name != params['fname']:
        change_dic = {"field": "fname", "old_value": user_auth.first_name, \
                      "new_value": params['fname']}
        audit_list.append(change_dic)
        user_auth.first_name = params['fname']
        
    if user_auth.last_name != params['sname']:
        change_dic = {"field": "sname", "old_value": user_auth.last_name, \
                      "new_value": params['sname']}
        audit_list.append(change_dic)
        user_auth.last_name = params['sname']
    if audit_list != []:
        try:
            user.save()
            user_auth.save()
            audit_created = audit_event(user, user,\
                                        AuditEventTypes.user_edited(), \
                                        list_of_changes = audit_list)
            if not audit_created:
                raise Exception
        except:            
            return failure_page(request, "Failed on user saving<br>")
    return saved_success(request)


def parse_inputs_personal(request):
    # Convert POST request parameters to dictionary
    param_dictionary = {}
    try:        
        if request.POST['birthdate'] == '':
            param_dictionary['birthdate'] = None
        else:
            param_dictionary['birthdate'] = \
                    parse(request.POST['birthdate']).strftime("%Y-%m-%d")
        param_dictionary['cellcountry'] = request.POST['cellcountry']
        param_dictionary['cellarea'] = request.POST['cellarea']
        param_dictionary['cellnum'] = request.POST['cellnumber']
        param_dictionary['addrcountry'] = request.POST['addrcountry']
        param_dictionary['addrpostid'] = request.POST['addrpostid']
        param_dictionary['addrtown'] = request.POST['addrcity']
        param_dictionary['addrstr'] = request.POST['addrstr']
        param_dictionary['addrhousenum'] = request.POST['addrhousenum']
        param_dictionary['addrapt'] = request.POST['addrapt']
        param_dictionary['addradditional'] = request.POST['addradditional']
        param_dictionary['fname'] = request.POST['fname']
        param_dictionary['sname'] = request.POST['sname']
    except KeyError:
        return -1 
    return param_dictionary
