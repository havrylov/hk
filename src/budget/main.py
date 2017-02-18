'''
Created on Jun 30, 2014

@author: thavr
'''

from budget.views import main_page, main_page2
from budget.debug import get_debug_user
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import date

@login_required(login_url='/login/')
def main(request):
    #<DEBUG SECTION>    
    user = get_debug_user(request)
    family = user.family
    #<DEBUG SECTION>
    return main_page(request, family, user)

@login_required(login_url="/login/")
def main2(request):
    #<DEBUG SECTION>    
    user = get_debug_user(request)
    family = user.family
    #<DEBUG SECTION>
    return main_page2(request, family, user)

@login_required
def give_necessary_statistics(request):
    
    user = get_debug_user(request)
    response_data = {"public_outcome" : 0, \
                     "public_income" : 0, \
                     "public_balance" : 0, \
                     "public_transaction_time" : 0, \
                     "private_outcome" : 0, \
                     "private_income" : 0, \
                     "private_balance" : 0, \
                     "private_transaction_time" : 0}
    response_data["public_outcome"] = user.get_family_outcome_sum()
    response_data["public_income"] = user.get_family_income_sum()
    response_data["public_balance"] = user.get_family_balance()
    first_transactions_datetime = user.get_first_transactions_datetime()
    if first_transactions_datetime is None:
        response_data["public_transaction_time"] = "Start Now!"
    else:
        response_data["public_transaction_time"] = \
                                            first_transactions_datetime.date()
    response_data["private_outcome"] = user.get_private_outcome_sum()
    response_data["private_income"] = user.get_private_income_sum()
    response_data["private_balance"] = user.get_private_balance()
    first_transactions_datetime = user.get_first_private_transactions_datetime()
    if first_transactions_datetime is None:
        response_data["private_transaction_time"] = "Start Now!"
    else:
        response_data["private_transaction_time"] = \
                                            first_transactions_datetime.date()
    return JsonResponse(response_data)