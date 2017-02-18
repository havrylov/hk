'''
Created on Jul 8, 2014

@author: thavr
'''
from budget.views import add_transactions, failure_page, saved_success,\
    transaction_edit_page, deleted_success
from budget.debug import get_debug_user
from budget.general import is_float, is_date
from dateutil.parser import parse
from budget.models import PublicTransaction, PrivatTransaction
from audit.service import audit_event
from audit.models import AuditEventTypes
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from __builtin__ import isinstance

def add_several(request):
    return add(request, True)

def add_one(request):
    return add(request, False)

@login_required(login_url="/login/")
def add(request, several):
    # <DEBUG SECTION>
    user = get_debug_user(request)
    # <DEBUG SECTION>
    return add_transactions(request, user, several)

@login_required(login_url="/login/")
def save_new_transactions(request, transact_params=[]):    
    if transact_params ==[]:
        # <DEBUG SECTION>
        user = get_debug_user(request)
        # <DEBUG SECTION>
        entries = request_to_array(request)
    else:
        user = transact_params[0]["user"]
        entries = transact_params
    if entries != []:
        for entry in entries:
            try:
                if entry['is_privat']:
                    transactionType = PrivatTransaction
                    audit_event_type = AuditEventTypes.private_transaction_created()
                else:
                    transactionType = PublicTransaction
                    audit_event_type = AuditEventTypes.transaction_created()
                new_transaction = transactionType(user = user, \
                                              transactionstime = entry['date'],\
                                              purpose = entry['purpose'], \
                                              comment = entry['comment'], \
                                              amount = entry['amount'])
                new_transaction.save()
                audit_created = audit_event(user, user,\
                                        audit_event_type, \
                                        transaction = new_transaction)
                if not audit_created:
                    raise Exception
            except Exception as exc:
                return failure_page(request, "Failed on transaction " + \
                                        str(entry) + " saving<br>" + str(exc))
    return saved_success(request)
        
            
            
def request_to_array(request, add_operation=True, edit_operation = False):
    outp = []
    if add_operation:
        index = 0
        try:
            trs_list = request.POST.getlist('date')
        except KeyError as exc:
            return []                 
        for val in trs_list:
            try:
                check_box_is_set = request.POST.getlist('amount')[index]
                is_private = True
            except KeyError as exc:
                is_private = False
            try: 
                entry = {'date':val, \
                         'amount':request.POST.getlist('amount')[index], \
                         'is_privat':is_private, \
                         'purpose':request.POST.getlist('purpose')[index], \
                         'comment':request.POST.getlist('comment')[index]}
                index = index + 1
                if is_float(entry['amount']) and is_date(entry['date']):
                        entry['date'] = parse(entry['date'])
                        entry['amount'] = float(entry['amount'])
                        outp.append(entry)
            except KeyError as exc:
                pass
        return outp
    
def edit_private_transaction(request):    
    return edit(request, is_private=True)

def edit_public_transaction(request):
    return edit(request, is_private=False)    

@login_required(login_url="/login/")
def edit(request, is_private):
    try:
        tr_id = request.GET['id']
    except KeyError:
        return redirect("budget:main")
    if not transaction_exists(tr_id):
        return redirect("budget:main")
    tr_belongs_to_user = user_is_allowed_to_edit(tr_id, request, is_private)
    if (not tr_belongs_to_user) or (tr_belongs_to_user == -1):
        return redirect("budget:main")
    return transaction_edit_page(request, tr_belongs_to_user)

@login_required(login_url="/login/")
def save_changes(request):    
    # <DEBUG SECTION>
    user = get_debug_user(request)
    # <DEBUG SECTION>
    try:
        initial_state = request.POST["is_private"]
    except KeyError as excpt:
        return failure_page(request, "incorrect POST data")
    if int(initial_state) == 1:
        private_transaction = True
        audit_event_type = AuditEventTypes.private_transaction_edited()
    elif int(initial_state) == 0:
        private_transaction = False
        audit_event_type = AuditEventTypes.transaction_edited()
    else:
        return failure_page(request, "incorrect POST data")
    
    try:
        private_flag = request.POST["private"]
        is_private = True        
    except KeyError as excpt:
        is_private = False    
        
    try:
        tr_id = request.POST["id"]
        amount = request.POST["amount"]
        date = request.POST["date"]
        purpose = request.POST["purpose"]
        comment = request.POST["comment"]
    except KeyError as excpt:
        return failure_page(request, "incorrect POST data")
    if not transaction_exists(tr_id):
        return failure_page(request, "Incorrect PublicTransaction ID")
    transaction = user_is_allowed_to_edit(tr_id, request, private_transaction)
    
    if private_transaction != is_private:
        transaction = change_transaction_type(transaction, \
                                              private_transaction, is_private)
        if isinstance(transaction, str):
            return failure_page(request, "Failed on transaction " + \
                                        transaction)    
    if transaction == -1:
        return failure_page(request, "Unknown error")
    if not transaction:
        return failure_page(request, "Attempt for edit unallowed transaction")
    if is_float(amount) and is_date(date):
        float_amount = float(amount)
        transactionstime = parse(date)
        audit_list = []
        
        if transaction.amount != float_amount:
            change_dic = {"field": "amount", "old_value": transaction.amount, \
                      "new_value": float_amount}
            audit_list.append(change_dic)
        transaction.amount = float_amount        
        
        transactionstime_tz_aware = timezone.make_aware(transactionstime, \
                                        timezone.get_current_timezone())
        
        if transaction.transactionstime != transactionstime_tz_aware:
            change_dic = {"field": "transactionstime", \
                          "old_value": transaction.transactionstime, \
                      "new_value": transactionstime}
            audit_list.append(change_dic)
        transaction.transactionstime = transactionstime_tz_aware
        
        if transaction.purpose != purpose:
            change_dic = {"field": "purpose", \
                          "old_value": transaction.purpose, \
                      "new_value": purpose}
            audit_list.append(change_dic)
        transaction.purpose = purpose
        
        if transaction.comment != comment:
            change_dic = {"field": "comment", \
                          "old_value": transaction.comment, \
                      "new_value": comment}
            audit_list.append(change_dic)
        transaction.comment = comment
        try:
            transaction.save()
        except Exception as exc:
            return failure_page(request, "Failed to save transaction " + \
                                "changes to DB")
        try:
            audit_created = audit_event(user, transaction.user, \
                                    audit_event_type, \
                                    transaction = transaction, \
                                    list_of_changes = audit_list)
            if not audit_created:
                raise Exception
        except Exception as exc:
            return failure_page(request, "Failed to save audit changes to DB")
        return saved_success(request)
    else:
        return failure_page(request, "Amount or Data parameters are incorrect")    
        

def transaction_exists(tr_id):
    try:
        transaction=PublicTransaction.objects.get(pk = tr_id)
    except PublicTransaction.DoesNotExist as exc:
        return False
    return True

def user_is_allowed_to_edit(tr_id, request, is_private): #DONE: Find out ow to define the user
    #DEBUG SECTION#
    user = get_debug_user(request)
    #DEBUG SECTION#
    if is_private:
        transaction_type = PrivatTransaction
    else:
        transaction_type = PublicTransaction
    user_list = user.get_all_members()
    try:
        transaction=transaction_type.objects.get(pk = tr_id)
    except Exception as exc:
        return -1
    if transaction.user in user_list: 
        return transaction
    else:
        return False
    
def change_transaction_type(transaction, current_state_is_private, \
                            new_state_is_private):
    if new_state_is_private:
        destination = PrivatTransaction
        audit_event_type_created = AuditEventTypes.private_transaction_created()
        audit_event_type_deleted = AuditEventTypes.transaction_deleted()
    else:
        destination = PublicTransaction
        audit_event_type_deleted = AuditEventTypes.private_transaction_deleted()
        audit_event_type_created = AuditEventTypes.transaction_created()
    try: 
        new_transaction = destination(user=transaction.user, \
                                transactionstime=transaction.transactionstime, \
                                purpose=transaction.purpose, \
                                comment=transaction.comment, \
                                amount=transaction.amount)
        new_transaction.save()
        audit_created = audit_event(transaction.user, transaction.user,\
                                    audit_event_type_created, \
                                    transaction = new_transaction)
        if not audit_created:
            raise Exception
    except Exception as exc:
        return str(exc)
    try:
        transaction.deleted = True
        transaction.save()
        audit_created = audit_event(transaction.user, transaction.user,\
                                    audit_event_type_deleted, \
                                    transaction = transaction)
        if not audit_created:
            raise Exception
    except Exception as exc:
        return str(exc)
    return new_transaction

@login_required(login_url="/login/")
def delete_transaction(request):
    # <DEBUG SECTION>
    user = get_debug_user(request)
    # <DEBUG SECTION>
    try:
        initial_state = request.POST["is_private"]
    except KeyError as excpt:
        return failure_page(request, "incorrect POST data")
    if int(initial_state) == 1:
        private_transaction = True
        audit_event_type = AuditEventTypes.private_transaction_deleted()
    elif int(initial_state) == 0:
        private_transaction = False
        audit_event_type = AuditEventTypes.transaction_deleted()
    else:
        return failure_page(request, "incorrect POST data")
    
    try:
        tr_id = request.POST["id"]        
    except KeyError as excpt:
        return failure_page(request, "incorrect POST data")
    
    if not transaction_exists(tr_id):
        return failure_page(request, "Incorrect ID")
    transaction = user_is_allowed_to_edit(tr_id, request, private_transaction)
    try:
        transaction.deleted = True
        transaction.save()
        audit_created = audit_event(transaction.user, transaction.user,\
                                    audit_event_type, \
                                    transaction = transaction)
        if not audit_created:
            raise Exception
    except Exception as exc:
        return failure_page(request, "Audit wasn't created" + str(exc))
    return deleted_success(request)