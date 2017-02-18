'''
Created on Jul 10, 2014

@author: thavr
'''
from budget.debug import get_debug_user
from django.http.request import HttpRequest
from budget.transactions import save_new_transactions

def create_request(date = "", amount = "13.65", purpose ="", comment = "", \
                   count = 1):
    request = HttpRequest()
    request.POST["date"] = [date]
    request.POST["amount"] = [amount]
    request.POST["purpose"] = [purpose]
    request.POST["comment"] = [comment]
    for i in range(count-1):
        request.POST["date"].append(date)
        request.POST["amount"].append(amount)
        request.POST["purpose"].append(purpose)
        request.POST["comment"].append(comment)
    return request
    

if __name__ == '__main__':
    user = get_debug_user()
    request = create_request(count=1)
    output = save_new_transactions(request)
    print output
    