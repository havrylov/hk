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
    from budget.models import PrivatTransaction, PublicTransaction
    all_tr = PrivatTransaction.objects.all().filter(deleted=False)
    trans_number = randint(0, len(all_tr))
    transaction = all_tr[trans_number]
    
    data = {'id': transaction.pk, 'amount':'-250', 'date': "Tue Jul 29 22:00:00 2014", \
            'purpose': 'I forgot about it...1', 'comment': '', 'is_private':'1'}
    test_user = transaction.user
    test_username = test_user.user.username
    
    c = Client()
    c.login(username = test_username, password = '12345678')    
    response = c.post('/save_changed_transaction', data)
    
    
    