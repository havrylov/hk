'''
Created on May 23, 2014

@author: thavr
'''

from django.conf.urls import patterns, url
from test_data import views, create_test_users, test_login


urlpatterns = [url(r'^$', views.start_page, name = 'start_page'),
                       url(r'^moving_forward', \
                           create_test_users.create_test_users, \
                           name = 'goahead'),
                       url(r'^login_test', test_login.login_test_user, \
                           name = 'login_test'),
                       url(r'^test_users', views.select_test_user, \
                           name = 'test_users')
                       ]