# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from budget.general import generate_confirmation_string
from budget.forms.form_create_user import CreateUserForm
from budget.forms.form_edit_user import EditUserForm
from budget.forms.form_edit_prefernces import EditPreferncesForm
from budget.debug import get_debug_user
from budget.forms.form_edit_access import EditAccess


def register(request, message = "Welcome to our community :)", \
             user_form = None, error_message = ""):
    if user_form == None:
        user_form = CreateUserForm()
    else:
        error_message = "Please correct the errors listed below."
    return render(request, "budget/create_user/register.html", \
                  {'message':message, 'form':user_form, \
                   'password_field':'id="password"', \
                   'retype_password': 'id="retypepassword"', \
                   'error_found': error_message})
    
def personal_settings(request, current_user, user_form=None, \
                      error_message = ""):   
    if user_form == None:
        intial_values = {'fname' : current_user.user.first_name,
                         'sname' : current_user.user.last_name,
                         'birthdate' : current_user.birthdate,
                         'cellcountry' : current_user.cellcountry,
                         'cellarea' : current_user.cellarea,
                         'cellnumber' : current_user.cellnum,
                         'addrcountry' : current_user.addrcountry,
                         'addrpostid' : current_user.addrpostid,
                         'addrcity' : current_user.addrtown,
                         'addrstr' : current_user.addrstr,
                         'addrhousenum' : current_user.addrhousenum,
                         'addrapt' : current_user.addrapt,
                         'addradditional' : current_user.addradditional}
        user_form = EditUserForm(initial = intial_values)
    else:
        error_message = "Please correct the errors listed below."
    return render(request, "budget/settings/personal_form.html", \
                  {'form':user_form, 'error_found': error_message, \
                   'user':current_user})
    
def site_preferences(request, current_user, user_form=None, \
                      error_message = ""):   
    if user_form == None:
        intial_values = current_user.get_user_settings_as_voc()
        user_form = EditPreferncesForm(initial = intial_values)
    else:
        error_message = "Please correct the errors listed below."
    return render(request, "budget/settings/personal_form.html", \
                  {'form':user_form, 'error_found': error_message, \
                   'user':current_user})    
    
def access_data(request, current_user, user_form=None, \
                      error_message = ""):   
    if user_form == None:
        intial_values = {'old_email' : current_user.user.email}
        user_form = EditAccess(initial = intial_values)
    else:
        error_message = "Please correct the errors listed below."
    return render(request, "budget/settings/access_form.html", \
                  {'form':user_form, 'error_found': error_message, \
                   'user':current_user})        

def show_mock(request, result=""):
    return render(request, "budget/showentries.html", \
                  {'request':request, 'result':result})

def failure_page(request, msg=""):
    message = "Pyzdets!<br>"+msg
    return HttpResponse(content = message, status=500)

def confirmation_success(request):
    return HttpResponse("The action was successfully confirmed!<br>" + \
                        "<br>Thank you!")
    
def start_page(request):    
    return login(request)

def login(request):
    return render(request, "budget/login_logout/login.html")

def logout (request):
    return render(request, "budget/login_logout/logout.html")

def main_page(request, family, user):
    return render(request, "budget/main/main.html", \
                  {'family':family, 'user':user})
    
def main_page2(request, family, user):
    return render(request, "budget/main/main2.html", \
                  {'family':family, 'user':user})
    
def func():
    return generate_confirmation_string()
    
def edit_wo_form(request, user):
    return render(request, "budget/settings/personal.html", \
                  {'user':user})
    
def family_setings(request, user):
    return render(request, "budget/settings/family.html", \
                  {'user':user})
    
def saved_success(request):
    return render(request, "budget/settings/changes_success.html")

def deleted_success(request):
    return render(request, "budget/settings/deletion_success.html")

def confirmation_resent_success(request):
    return render(request, "budget/confirmation/confirmation_resend.html")

def add_transactions(request, user, several):
    number_of_rows = 10
    if several: 
        tmplt = "budget/transactions/add.html"
    else:
        tmplt = "budget/transactions/add_nomenu.html"
    return render(request, tmplt, {'user':user, \
                                   'rows_number':list(range(number_of_rows)), \
                                   'max_row_num':number_of_rows})
    
def search_page(request, user):
    from budget.ajax import search_result
    resulting_grid = search_result(request)
    return render(request, "budget/search/search.html", \
                  {'user':user, 'search_function': resulting_grid})

def no_more_confirmations_today(request):
    return render(request, "budget/service/no_more_conf.html")

def return_search_function(request):
    from budget.ajax import search_result
    return render(request, "budget/search/search_result.html",
                  {'search_function':search_result(request)})

def register_success(request, user_info):
    try:
        users = user_info[2]
    except:
        return failure_page(request)
    fullname = users.get_full_name()
    if fullname != users.user.get_full_name():
        fullname = 'Sir or Madam'
    
    return render(request, 'budget/create_user/register_success.html',\
                  {'username':fullname, 'email':users.user.email})
    
def something(request):
    current_site = get_current_site(request)
    return HttpResponse("current_site.domain " + current_site.domain + "<br>"+\
                        "current_site.name " + current_site.name + "<br>"+\
                        "request.path " + request.path + "<br>"+\
                        "HttpRequest.get_host() " + request.get_host())
    
def transaction_edit_page(request, transaction):
    return render(request, "budget/transactions/edit_nomenu.html", \
                  {'transaction':transaction})
    
def test_bed(request):
    return render (request, "budget/test_bed/tz1.html")

def initial_graphics(request):
    return render(request, "budget/statistics/initial_graphs.html")
