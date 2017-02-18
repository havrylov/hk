'''
Created on Sep 25, 2015

@author: thavr
'''
from test_data.forms.form_create_test_users import CreateTestUsersForm
from test_data.views import start_page
from django.http.response import HttpResponse
from test_data.models import InitialNames
from random import seed, randint
from budget.create_user import user_creation_procedure
from time import time
from datetime import datetime
from budget.models import Users
from budget.transactions import save_new_transactions
from django.contrib.auth import login,authenticate


def create_test_users(request):
    if request.method == 'POST':
        create_test_user_form = CreateTestUsersForm(request.POST)
        if create_test_user_form.is_valid(): 
            response = create_test_users_procedure(request)
            if response:
                return response
    else:
        create_test_user_form = CreateTestUsersForm() # An unbound form

    return start_page(request, user_form=create_test_user_form)

def create_test_users_procedure(request):
    seed()
    names = ''
    for current_user in range(int(request.POST['users'])):
        test_name = generate_name()
        email = generate_email(test_name).lower()
        is_generated = generate_users(test_name, email, request) #TODO: This is not true!!!!
        min_transactions = int(request.POST['min_transactions'])
        max_transactions = int(request.POST['max_transactions'])
        num_of_transactions = randint(min_transactions, max_transactions)
        if num_of_transactions == 0:
            continue
        try:
            user = Users.objects.get(pk = current_user + 1)
        except Exception as e:
            continue
        transact_params = {}
        transact_params["comment"] = ""
        transact_params["user"] = user
        uu = authenticate(username=user.user.username, password="12345678")
        login(request, uu)        
        privat_flag = False
        for current_transaction in range(num_of_transactions):            
            transact_params["date"] = generate_date()
            transact_params["amount"] = generate_amount()
            transact_params["is_privat"] = privat_flag
            if privat_flag:
                privat_flag = False
            else:
                privat_flag = True
            if transact_params["amount"] > 0:
                transact_params["purpose"] = name_the_entry(False)
            else:
                transact_params["purpose"] = name_the_entry(True)
            transaction_created = save_new_transactions(request, \
                                                        [transact_params])
        names = names +"<br>" + test_name[0]+" "+test_name[1]+ "has " +\
         str(num_of_transactions) + "transactions."
    return HttpResponse(names)

def generate_users(user_name, email, request):
    password = "12345678"
    user_params = {'birthdate':None,\
                       'cellcountry':'',\
                       'cellarea':'', \
                       'cellnum':'', \
                       'addrcountry':'', \
                       'addrpostid':'', \
                       'addrtown':'', \
                       'addrstr':'',\
                       'addrhousenum':'',\
                       'addrapt':'',  \
                       'addradditional':'',\
                       'family_email':'', \
                       'email':email, \
                       'password':password, \
                       'fname':user_name[0], \
                       'sname':user_name[1]}
    result = user_creation_procedure(request, user_params)
    return result
    
    
    
def generate_name():
    seed()
    length_of_nnames_db = len(InitialNames.objects.all())
    fname = InitialNames.objects.get(pk = randint(1,length_of_nnames_db)).first_name
    sname = InitialNames.objects.get(pk = randint(1,length_of_nnames_db)).last_name
    return [fname, sname]

def generate_email(user_name):
    [fname, sname]=user_name
    seed()
    domain = ""
    for i in range(10):
        domain += chr(randint(97,122))
        
    email = fname+sname+"@"+domain+".com"
    return email

def name_the_entry(is_expense):
    expenses = ["Rent or mortgage", "Homeowner's or renter's insurance", \
                "Home warranty", "Home maintenance/repairs", "Lawn care", \
                "Property taxes", "Car payment", "Fuel", "Auto insurance", \
                "Tires and maintenance", "Tag/registration", "Electric bill", \
                "Water bill", "Gas bill", "Phone bill", "Internet service", \
                "Cable or satellite service", "Groceries", "Dining out", \
                "Clothing", "Hair care", "Medical expenses", "Gym membership", \
                "Vacation", "Charitable giving", "Entertainment", "Gifts"]
    incomes = ["Salary", "Rate", "Gift", "Sale", "Debts returned", "Refund", \
               "Return", "Lotto", "Other"]
    if is_expense:
        list_of_names = expenses
    else:
        list_of_names = incomes
    seed()
    return list_of_names[randint(0, len(list_of_names)-1)]

def generate_amount():
    seed()
    return float(randint(-2000000, 2000000))/100

def generate_date():
    seed()
    return datetime.fromtimestamp(randint(1, int(time())))