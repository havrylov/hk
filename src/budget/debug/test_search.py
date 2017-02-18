'''
Created on Jul 28, 2014

@author: thavr
'''

import django


if __name__ == '__main__':
    django.setup()
    from django.test import Client
    from budget.models import Users
    test_user_id = 1
    test_user = Users.objects.get(pk=test_user_id)
    test_username = test_user.user.username
    
    c = Client()
    c.login(username = test_username, password = '12345678')
    
    print c.get("/search?income=1")
    
