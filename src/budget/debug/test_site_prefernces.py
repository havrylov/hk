'''
Created on Aug 19, 2014

@author: thavr
'''
from random import seed, randint
import django

if __name__ == '__main__':
    django.setup()
    seed()    
    from django.test.client import Client
    from budget.models import Users
    test_user = Users.objects.get(pk=5)
    
    data = {'start_tab': 'priv'}
    test_username = test_user.user.username
    
    c = Client()
    c.login(username = test_username, password = '12345678')    
    response = c.post('/save_preferences', data)
    
    
    