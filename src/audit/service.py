'''
Created on Jul 29, 2014

@author: thavr
'''
from audit.models import AuditEvent, AuditEventTypes, TransactionChange,\
    UserChange, PreferencesChange
from django.utils import timezone

def audit_event(user_init, user_impact, event_type, \
                transaction=None, confirmation = None, list_of_changes=[]):
    if transaction != None:
        transaction = str(transaction.pk)
    if confirmation != None:
        confirmation = str(confirmation.pk)
    #try:    
    new_event = AuditEvent(user_initiated= user_init, \
                               user_impacted = user_impact, \
                               event_type = event_type, \
                               event_date = timezone.now(), \
                               transaction = transaction, \
                               confirmation = confirmation)
    new_event.save()
    #except:
    #    return False
    
    if event_type == AuditEventTypes.transaction_edited():
        tr_tracking = track_transaction_change(new_event, list_of_changes)
        if tr_tracking == -999:
            return False    
    elif event_type == AuditEventTypes.user_edited():
        user_tracking = track_user_change(new_event, list_of_changes)
        if user_tracking == -999:
            return False
    elif event_type == AuditEventTypes.site_preferences_edited():
        user_tracking = track_preferences_change(new_event, list_of_changes)
        if user_tracking == -999:
            return False
        
        
    return True
        
def track_transaction_change(event, list_of_changes):
    track_type = TransactionChange
    result = track_change(event, track_type, list_of_changes)
    if not result:
        return -999
    return result
    

def track_user_change(event, list_of_changes):
    track_type = UserChange
    result = track_change(event, track_type, list_of_changes)
    if not result:
        return -999
    return result

def track_preferences_change(event, list_of_changes):
    track_type = PreferencesChange
    result = track_change(event, track_type, list_of_changes)
    if not result:
        return -999
    return result

def track_change(event, tracking_type, list_of_changes):
    for change in list_of_changes:
        #try:
        changed_value = change["field"]
        was = change["old_value"]
        become = change["new_value"]
        #except KeyError:
        #    return False
        #try:
        new_tracking = tracking_type(audit_event = event, \
                                 field_changed = changed_value, \
                                 old_value = was, \
                                 new_value = become)
        new_tracking.save()
        #except:
            #return False
    return True

    

