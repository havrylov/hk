from django.db import models

class Transaction(models.Model):
#     Class designed to store the information about each single 
#     transaction
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transactionstime = models.DateTimeField()
    purpose = models.CharField(max_length = 255, blank = True)
    comment = models.CharField(max_length = 255, blank = True, null = True)
    deleted = models.BooleanField(default = False)
    
    def is_private(self):
        return False
    
    def is_public(self):
        return True
    
    def is_income(self):
        if self.amount >= 0:
            return True
        return False 
    
    def is_outcome(self):
        return not self.is_income()
    
    def get_user(self):
        return self.users.get_full_name()
    
    def show_local_time_presentation(self):
        return self.transactionstime.strftime("%c")
    
    def __unicode__(self):
        return self.purpose+";"+str(self.amount)+";"\
            +str(self.transactionstime)