'''
Created on Jul 23, 2014

@author: thavr
'''
from budget.debug import get_debug_user
from django.db.models import Max, Min
from budget.models import User, Users
from budget.views import show_mock
from dateutil.parser import parse
import datetime
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def search_result(request):
    ##DEBUG
    user = get_debug_user(request)
    ##DEBUG        
    search_criterium = parse_request(request)
    empty_set = []
    if search_criterium["give_no_result"]:
        return empty_set
    output_set = get_initial_transactions_set(request)
    if is_empty(output_set):
        return empty_set    
    if search_criterium["show_outcome"] and search_criterium["show_income"]:
        pass
    elif search_criterium["show_outcome"]:
        output_set = return_only_outcome(output_set)
    elif search_criterium["show_income"]:
        output_set = return_only_income(output_set)
    
    if is_empty(output_set):
        return empty_set
                
    output_set = filter_transactions_by_amount(output_set,\
                            min_amount = search_criterium["min_amount"], \
                            max_amount = search_criterium["max_amount"])
    
    if is_empty(output_set):
        return empty_set
    
    output_set = filter_transactions_by_date(output_set,\
                            before = search_criterium["before"], \
                            after = search_criterium["after"])
    
    if is_empty(output_set):
        return empty_set
    
    output_set = filter_transactions_by_users(output_set,\
                            users = search_criterium["users"])
    
    if is_empty(output_set):
        return empty_set
    
    output_set = filter_transactions_by_purpose(output_set,\
                            value=search_criterium["purpose"], \
                            exact=search_criterium["purpose_exact"])
    
    if is_empty(output_set):
        return empty_set
    
    output_set = filter_transactions_by_comment(output_set,\
                            value=search_criterium["comment"], \
                            exact=search_criterium["comment_exact"])
    
    return order_by_time(output_set)

def is_empty(input_set):
    flag = True
    for current_set in input_set:
        if len(current_set) > 0:
            flag = False
    return flag
    
@login_required(login_url="/login/")    
def get_initial_transactions_set(request):
    ##DEBUG
    user = get_debug_user(request)
    ##DEBUG
    return [user.get_all_public_family_transactions(), \
            user.get_all_privat_user_transactions()]

# -----------------------------Section of amount--------------------------------

def filter_transactions_by_amount(transactions, \
                                  min_amount = "", \
                                  max_amount = ""):
    if min_amount =="":
        min_amount = -9999999999.99
    if max_amount == "":
        max_amount = 9999999999.99
    prom_res = [transaction.filter(amount__gte=min_amount).\
                filter(amount__lte=max_amount) for transaction in transactions]    
    return prom_res

def return_only_income(transactions):
    return filter_transactions_by_amount(transactions, min_amount=0)

def return_only_outcome(transactions):
    return filter_transactions_by_amount(transactions, max_amount=0)
# -----------------------------End of Section of amount-------------------------

# -----------------------------Section of date----------------------------------
def filter_transactions_by_date(transactions, \
                                  before = "", \
                                  after = ""):
    if before == "" and after=="":
        return transactions
    elif after == "":
        return [transaction.filter(transactionstime__lte = before) \
                             for transaction in transactions]
    elif before == "":
        return [transaction.filter(transactionstime__gte = after)  \
                             for transaction in transactions]
    else:
        return [transaction.filter(transactionstime__gte = after).\
            filter(transactionstime__lte = before) \
                             for transaction in transactions]

# -----------------------------End of Section of date---------------------------

# -----------------------------Section of text search---------------------------
def filter_transactions_by_text_parameter(transactions, field, \
                                          value="", exact=False):
    if value == "":
        return transactions
    if exact:
        if field == "purpose":
            return [transaction.filter(purpose__iexact=value) \
                             for transaction in transactions]
        elif field == "comment":
            return [transaction.filter(comment__iexact=value) \
                             for transaction in transactions]
        else:
            raise KeyError
    else:
        if field == "purpose":
            return [transaction.filter(purpose__icontains = value) \
                             for transaction in transactions]
        elif field == "comment":
            return [transaction.filter(comment__icontains=value) \
                             for transaction in transactions]
        else:
            raise KeyError
# -----------------------------End section of text search-----------------------

# -----------------------------Section of purpose-------------------------------

def filter_transactions_by_purpose(transactions,  \
                                          value="", exact=False):
    
    return filter_transactions_by_text_parameter(transactions, "purpose", \
                                                 value=value, exact=exact)

# -----------------------------End of Section of purpose------------------------

# -----------------------------Section of comment-------------------------------

def filter_transactions_by_comment(transactions,  \
                                          value="//", exact=False):
    
    return filter_transactions_by_text_parameter(transactions, "comment", \
                                                 value=value, exact=exact)

# -----------------------------End of Section of comment------------------------

# -----------------------------Section of users---------------------------------

def filter_transactions_by_users(transactions, users = []):
    
    # NOTE!!! users is ALREADY list of Users objects
    if users == []:
        return transactions
    return [transaction.filter(user__in = users) \
                             for transaction in transactions]

# -----------------------------End section of users---------------------------------
# -----------------------------Section of auxilaries----------------------------
def get_border_value_of_transactions(user, border = "max", \
                                         criterium = "transactionstime"):
        tr = user.get_all_public_family_transactions()
        if border == "max":
            tr1 = tr.aggregate(Max(criterium))
            return tr1[criterium+"__max"]
        elif border == "min":
            tr1 = tr.aggregate(Min(criterium))
            return tr1[criterium+"__min"]
        
        raise KeyError
    
def get_max_value_of_transaction(user, criterium = "transactionstime"):
        return get_border_value_of_transactions(user, border = "max", \
                                                     criterium = criterium)
    
def get_min_value_of_transaction(user, criterium = "transactionstime"):
        return get_border_value_of_transactions(user, border = "min", \
                                                     criterium = criterium)

@login_required(login_url="/login/")        
def parse_request(request):
    ##DEBUG
    user = get_debug_user(request)
    ##DEBUG
    output = {}
    try:
        after = request.GET["begin"]
    except KeyError:
        after = get_min_value_of_transaction(user, "transactionstime")
    
    if after != "":
        try:
            after = parse(after)
        except:
            after = ""
        
    output["after"] = after
    
    try:
        before = request.GET["end"]
    except KeyError:
        before = get_max_value_of_transaction(user, "transactionstime")
        
    if before != "":
        try:
            before = parse(before)
        except:
            before = ""
    output["before"] = before
    
    try:
        max_amount = request.GET["maxamount"]
    except KeyError:
        max_amount = get_max_value_of_transaction(user, "amount")
    try:
        float(max_amount)
    except ValueError:
        max_amount = ""
    except TypeError:
        max_amount = ""
    output["max_amount"] = max_amount
    
    try:
        min_amount = request.GET["minamount"]
    except KeyError:
        min_amount = get_min_value_of_transaction(user, "amount")
    try:
        float(min_amount)
    except ValueError:
        min_amount = ""
    except TypeError:
        min_amount = ""
    output["min_amount"] = min_amount
    
#     try:
#         show_private = request.GET["private"]
#         output["show_private"] = True
#     except KeyError:
#         output["show_private"] = False
#         
#     try:
#         show_private = request.GET["public"]
#         output["show_public"] = True
#     except KeyError:
#         output["show_public"] = False
    
    try:
        show_income = request.GET["income"]
        output["show_income"] = True
    except KeyError:
        output["show_income"] = False  
        
    try:
        give_no_result = request.GET["nosearch"]
        output["give_no_result"] = True
    except KeyError:
        output["give_no_result"] = False  
    
    try:
        show_outcome = request.GET["outcome"]
        output["show_outcome"] = True
    except KeyError:
        output["show_outcome"] = False
    
    try:
        users = request.GET.getlist('users')
        output["users"] = []
        for user_email in users:
            try:
                user_auth = User.objects.get(email = user_email)
                user = Users.objects.get(user = user_auth)
                output["users"].append(user)
            except User.DoesNotExist:
                pass
            except Users.DoesNotExist:
                pass
    except KeyError:
        output["users"] = []        
        
    output["purpose_exact"] = define_exact("purposecomparation", request)
    output["comment_exact"] = define_exact("commentcomparation", request)
    output["purpose"] = define_text("purpose", request)
    output["comment"] = define_text("comment", request)
    

    return output 

def define_exact(parameter, request):
    try:
        exact = request.GET[parameter]
        if exact == "equals":
            return True
        else:
            return False
    except KeyError:
        return False
    
def define_text(parameter, request):
    try:
        text = request.GET[parameter]
        return text
    except KeyError:
        return ""    
    
def order_by_time(transactions, asc=False):
    if asc:
        param = "transactionstime"
    else:
        param = "-transactionstime"
    return [transaction.order_by(param)  \
                             for transaction in transactions]
    
    
    
    
            
        
# -----------------------------End Section of auxilaries------------------------        