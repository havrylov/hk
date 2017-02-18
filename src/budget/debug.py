'''
Created on Jul 9, 2014

@author: thavr
'''

from budget.models import User, Users

def get_debug_user(request=None):
    if request is None:
        user=User.objects.filter(pk = 1)[0]
    else:
        user = Users.objects.get(user = request.user)
    return user

