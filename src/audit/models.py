from django.db import models
from budget.models import Users
from constants.text_constants import *


# Create your models here.

class AuditEventTypes(models.Model):
    event_type = models.CharField(max_length = 40)    
    user_created = constant_user_created                
    user_edited = constant_user_edited                 
    user_deleted = constant_user_deleted                 
    transaction_created = constant_transaction_created          
    transaction_edited = constant_transaction_edited           
    transaction_deleted = constant_transaction_deleted
    private_transaction_created = constant_private_transaction_created          
    private_transaction_edited = constant_private_transaction_edited           
    private_transaction_deleted = constant_private_transaction_deleted           
    family_confirmation_sent = constant_family_confirmation_sent   
    family_confirmed = constant_family_confirmed             
    email_confiration_sent = constant_email_confiration_sent       
    email_confirmed = constant_email_confirmed              
    email_confirmation_expired = constant_email_confirmation_expired   
    family_confirmation_expired = constant_family_confirmation_expired
    site_preferences_edited = constant_site_preferences_changed
    unknown_event = constant_unknown_event
    
    event_types = [user_created, user_edited, user_deleted, \
                   transaction_created, transaction_edited, \
                   transaction_deleted, private_transaction_created, \
                   private_transaction_edited, private_transaction_deleted, \
                   family_confirmation_sent, family_confirmed, \
                   email_confiration_sent, email_confirmed, \
                   email_confirmation_expired, family_confirmation_expired, 
                   site_preferences_edited, unknown_event]
    
    @classmethod
    def user_created(c):
        return c.objects.get(event_type = constant_user_created)
    
    @classmethod
    def user_edited(c):
        return c.objects.get(event_type = constant_user_edited)
    
    @classmethod
    def user_deleted(c):
        return c.objects.get(event_type = constant_user_deleted)
    
    @classmethod
    def transaction_created(c):
        return c.objects.get(event_type = constant_transaction_created)
    
    @classmethod
    def transaction_edited(c):
        return c.objects.get(event_type = constant_transaction_edited)
    
    @classmethod
    def transaction_deleted(c):
        return c.objects.get(event_type = constant_transaction_deleted)
    
    @classmethod
    def private_transaction_created(c):
        return \
            c.objects.get(event_type = constant_private_transaction_created)
    
    @classmethod
    def private_transaction_edited(c):
        return \
            c.objects.get(event_type = constant_private_transaction_edited)
    
    @classmethod
    def private_transaction_deleted(c):
        return \
            c.objects.get(event_type = constant_private_transaction_deleted)
    
    @classmethod
    def family_confirmation_sent(c):
        return \
            c.objects.get(event_type = constant_family_confirmation_sent)
    
    @classmethod
    def family_confirmed(c):
        return c.objects.get(event_type = constant_family_confirmed)
    
    @classmethod
    def email_confiration_sent(c):
        return c.objects.get(event_type = constant_email_confiration_sent)
    
    @classmethod
    def email_confirmed(c):
        return c.objects.get(event_type = constant_email_confirmed)
    
    @classmethod
    def email_confirmation_expired(c):
        return \
            c.objects.get(event_type = constant_email_confirmation_expired)
    
    @classmethod
    def family_confirmation_expired(c):
        return \
            c.objects.get(event_type = constant_family_confirmation_expired)
            
    @classmethod
    def site_preferences_edited(c):
        return c.objects.get(event_type = constant_site_preferences_changed)
    
    @classmethod
    def unknown_event(c):
        return c.objects.get(event_type = constant_unknown_event)
    
    
class AuditEvent(models.Model):
    user_initiated = models.ForeignKey(Users, related_name = "initiator")
    user_impacted = models.ForeignKey(Users, related_name = "victim")
    event_type = models.ForeignKey(AuditEventTypes)
    event_date = models.DateTimeField()
    transaction = models.CharField(max_length = 20, blank = True, \
                                   null = True, default = None)
    confirmation = models.CharField(max_length = 20, blank = True, \
                                    null = True, default = None)
    
    
    
class TransactionChange(models.Model):
    audit_event = models.ForeignKey(AuditEvent)
    field_changed = models.CharField(max_length = 50)
    old_value = models.CharField(max_length = 255, null = True)
    new_value = models.CharField(max_length = 255)
    
class UserChange(models.Model):
    audit_event = models.ForeignKey(AuditEvent)
    field_changed = models.CharField(max_length = 20)
    old_value = models.CharField(max_length = 255, null = True)
    new_value = models.CharField(max_length = 255)   
    
class AccessDataChange(models.Model):
    user_impacted = models.ForeignKey(Users)
    pasword_change= models.BooleanField(default = False)
    email_change= models.BooleanField(default = False)
    change_date = models.DateTimeField()
    password_verification_result=models.CharField(max_length = 10) 
    
class PreferencesChange(models.Model):
    audit_event = models.ForeignKey(AuditEvent)
    field_changed = models.CharField(max_length = 50)
    old_value = models.CharField(max_length = 255, null = True)
    new_value = models.CharField(max_length = 255)    