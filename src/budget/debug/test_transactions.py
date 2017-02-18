'''
Created on Jul 15, 2014

@author: thavr
'''
from budget.debug import get_debug_user
import django


if __name__ == '__main__':
    django.setup()
    u2 = get_debug_user()
    u2.transaction_set.create(amount = -35.33, purpose = "Dinner with wife", \
                              transactionstime = "2013-01-01 23:59:00Z", \
                              comment = "")
    u2.transaction_set.create(amount = 35.33, purpose = "Bank rate", \
                              transactionstime = "2012-12-31 13:27:00Z", \
                              comment = "Bank of America")
    u2.transaction_set.create(amount = -36.33, purpose = "Pertol", \
                              transactionstime = "2013-02-15 12:59:00Z", \
                              comment = "ARAL")
    u2.transaction_set.create(amount = 36.33, purpose = "Money-back from amazon",\
                               transactionstime = "2012-01-01 00:00:01-08:00", \
                               comment = "")
    
    print "OK"
