'''
Created on Jul 15, 2014

@author: thavr
'''
def order_transactions(transactions_set, \
                       criterium = "transactionstime",
                       descending = True):
    
    allowed_criterium= ['id', 'user', 'amount', 'transactionstime', 'purpose', \
                        'comment']
    
    if criterium not in allowed_criterium:
        return -4
    if descending:
        criterium = "-"+ criterium
    try:
        output = transactions_set.order_by(criterium)
    except:
        return -5  
    return output
