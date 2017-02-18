'''
Created on Jul 15, 2014

@author: thavr
'''
from budget.debug import get_debug_user
from django.contrib.auth.decorators import login_required
#from budget.views import search_page

@login_required(login_url="/login/")
def search(request):
    from budget.views import search_page
    ##DEBUG
    user = get_debug_user(request)
    ##DEBUG
    return search_page(request, user)

