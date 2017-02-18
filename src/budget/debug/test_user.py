'''
Created on Aug 24, 2014

@author: thavr
'''

'''
Created on Aug 19, 2014

@author: thavr
'''
from django.test.client import Client
data = {'email': '123@qwe.com', 'password':'1', 'retypepassword': "1"}
c=Client()
print c.post('/showregistration', data)
    
    
    
    
    