'''
Created on Jul 29, 2014

@author: thavr
'''
from audit.models import AuditEventTypes

if __name__ == '__main__':
    for event in AuditEventTypes.event_types:
        try:
            oet = AuditEventTypes.objects.get(event_type = event)
        except AuditEventTypes.DoesNotExist:                
            aet = AuditEventTypes(event_type = event)
            aet.save()
    print "OK"