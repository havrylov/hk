'''
Created on May 23, 2014

@author: thavr
'''

from django.conf.urls import url
from budget import views, create_user, confirmation, \
    login, main, settings, transactions, search, ajax, access_settings, \
    graphics, site_prefernces


urlpatterns = [url(r'^test_bed', views.test_bed, name='test_bed'),
               url(r'^test$', views.something, name='smth'),
               url(r'^parse', transactions.request_to_array, name='parse'),
               url(r'^debug_request', ajax.search_result, name='debug_request'),
               url(r'^newuser', views.register, name='newuser'),
               url(r'^showregistration', \
                create_user.user_creation_procedure_with_form, name='register'),
               url(r'^confirm$', confirmation.confirmation_procdedure, \
                   name='confirm'),
               url(r'^login', views.login, name='login'),
               url(r'^$', views.start_page, name='start_page'),
               url(r'^logout', login.logout_user, name='logout'),
               url(r'^signin', login.signin, name='signin'),
               url(r'^main/$', main.main, name='main'),
               url(r'^main2', main.main2, name='main2'),
               url(r'^personal$', settings.personal, name='personal'),
               url(r'^access$', settings.access, name='access'),
               url(r'^save$', settings.user_edit_form_validation, name='save'),
               url(r'^add_transactions$', transactions.add_several, \
                   name='add_tr_menu'),
               url(r'^add_transaction$', transactions.add_one, \
                   name='add_tr_page'),
               url(r'^speicher_transactions', \
                   transactions.save_new_transactions, name='speicher_tr'),
               url(r'^email_resend', confirmation.resend_email_confirmation, \
                           name='email_resend'),
               url(r'^family_resend', confirmation.resend_family_confirmation, \
                           name='family_resend'),
               url(r'^search$', search.search, name='search'),
               url(r'^filter_results$', views.return_search_function, \
                           name='filter'),
               url(r'^family_settings', settings.family, name='family_settings'),
               url(r'^save_family_settings', settings.save_family_pseudos, \
                           name='save_family_settings'),
               url(r'^save_access_settings', \
                           access_settings.user_access_edit_form_validation, \
                           name='save_access_settings'),
               url(r'^edit_transaction', transactions.edit, \
                   name='edit_transaction'),
               url(r'^edit_public_transaction', \
                   transactions.edit_public_transaction, \
                   name='edit_public_transaction'),
               url(r'^edit_private_transaction', \
                           transactions.edit_private_transaction, \
                           name='edit_private_transaction'),                       
               url(r'^save_changed_transaction', transactions.save_changes, \
                           name='save_changed_transaction'),                       
               url(r'^delete_transaction', transactions.delete_transaction, \
                           name='delete_transaction'),
               url(r'^give_user_statistic', main.give_necessary_statistics, \
                           name='statistic'),
               url(r'^main_graphics', graphics.main_graphics, name='graphics'),
               url(r'^preferences', site_prefernces.preferences, \
                           name='preferences'),
               url(r'^save_preferences', \
                   site_prefernces.change_site_prefernces, \
                   name='save_preferences')
               ]