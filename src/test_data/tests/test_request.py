'''
Created on Sep 25, 2015

@author: thavr
'''
import django
from django.test.client import Client
if __name__ == '__main__':
    django.setup()    
    data = {'users':'3', 'min_transactions':"2", 'max_transactions':'4'}
    c=Client()
    print c.post('/test_data/moving_forward', data)