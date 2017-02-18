'''
Created on Jul 30, 2014

@author: thavr
'''
from django.test.client import Client
if __name__ == '__main__':
    data = {'fname' : 'Abanga', 'sname' : 'Maksimov', 'birthdate' : '', \
    'cellcountry' : '', 'cellarea' : '172', 'cellnumber' : '', \
    'addrcountry' : 'Germany', 'addrpostid' : '', 'addrcity' : '', \
    'addrstr' : '', 'addrhousenum' : '', 'addrapt' : '', \
    'addradditional' : 'http%3A%2F%2Fxxx.com%2Fbudget%2Fconfirm%3Femail%3Dnpys%40zbkj.com%26code%3Dccdf4307d3653a9d37c25af1eea9f03d'}
    c=Client()
    print c.post('/save', data)

