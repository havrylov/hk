from django.db import models
from django.db.models import Min
from django.contrib.auth.models import User
from budget.transactions_filtering import order_transactions


class Family(models.Model):
    founder = models.EmailField(max_length=255, unique=True)
    
    def get_all_members(self):
        all_members = Users.objects.filter(family = self).\
        filter(famidconfirmed=True)
        return all_members

class Users(models.Model):
    user = models.OneToOneField(User)
    family = models.ForeignKey(Family)
    emailisconfirmed = models.BooleanField(default = False)
    birthdate = models.DateField(null = True)
    regdate = models.DateTimeField()
    famidconfirmed = models.BooleanField(default = False)
    cellcountry = models.CharField(max_length=255, blank = True, \
                                   null = True)
    cellarea = models.CharField(max_length=255, blank = True,null = True)
    cellnum = models.CharField(max_length=255, blank = True,null = True)
    addrcountry = models.CharField(max_length=255, blank = True, \
                                   null = True)
    addrpostid = models.CharField(max_length=255, blank = True, \
                                  null = True)
    addrtown = models.CharField(max_length=255, blank = True, null = True)
    addrstr = models.CharField(max_length=255, blank = True, null = True)
    addrhousenum = models.CharField(max_length=255, blank = True, \
                                    null = True)
    addrapt = models.CharField(max_length=255, blank = True, null = True)
    addradditional = models.CharField(max_length=255, blank = True, \
                                      null = True)
    
    def __unicode__(self):
        return self.get_full_name()
    
    def get_pseudonym_for_me(self, user):
        try:
            pseudo = Pseudonym.objects.filter(for_the_user=self)
            pseudo = pseudo.get(of_the_user = user)
        except Pseudonym.DoesNotExist:
            return None
        return pseudo
    
    def get_pseudonym_of_me(self, user):
        try:
            pseudo = Pseudonym.objects.filter(for_the_user=user)
            pseudo = pseudo.get(of_the_user = self)
        except Pseudonym.DoesNotExist:
            return None
        return pseudo
    
    def get_all_pseudos_except_mine(self):
        pseudonyms = {}
        family_users = self.get_all_members()
        for family_user in family_users:
            if family_user != self:
                pseudo = self.get_pseudonym_for_me(family_user)
                if pseudo == None:
                    pseudo = False
                pseudonyms[family_user] = pseudo
        return pseudonyms
    
    def get_full_name(self):
        
        fullname = self.user.get_full_name()
        
        if fullname == '':
            fullname = "User '"+self.user.email+"'"
        return fullname
    
    def get_all_members(self):
        if self.famidconfirmed:
            family = self.family
            return family.get_all_members()
        else:
            return [self]
        
    def is_family_not_empty(self):
        if len(self.get_all_members()) <= 1:
            return False
        else:
            return True
        
    def get_all_public_family_transactions(self):
        transactions = PublicTransaction.objects.\
            filter(user__in=self.get_all_members())
        transactions=transactions.filter(deleted = False)
        return transactions
    
    def get_all_privat_user_transactions(self):
        transactions = PrivatTransaction.objects.filter(user=self)
        transactions=transactions.filter(deleted = False)
        return transactions
    
    def get_all_available_user_transaction(self):
        pass
    
    def get_all_requested_transactions(self, trans_type):
        if trans_type == "public":
            all_transactions = self.get_all_public_family_transactions()
        elif trans_type == "private":
            all_transactions = self.get_all_privat_user_transactions()
        else:
            return -1
        return all_transactions
    
    def search_criterium_by_date_desc(self, request):
        pass
    
    def filter_transactions_amount_less_than(self, amount_less, \
                                             transactions_set="",
                                             trans_type="public"):
        if transactions_set == "":
            transactions_set = self.get_all_requested_transactions(trans_type)
        if transactions_set == -1:
            return -1
        return transactions_set.filter(amount_lt=amount_less)


    def get_all_income(self, trans_type="public"):
        all_transactions = self.get_all_requested_transactions(trans_type)
        if all_transactions == -1:
            return -2
        all_income = all_transactions.filter(amount__gte=0)
        return all_income
    
    def get_all_outcome(self, trans_type="public"):
    
        all_transactions = self.get_all_requested_transactions(trans_type)
        if all_transactions == -1:
            return -3
        all_income = all_transactions.filter(amount__lt=0)
        return all_income
    
    def get_last_n_incomes(self, trans_type = 'public', n=5):
        all_incomes = order_transactions(self.get_all_income(trans_type))
        return all_incomes[:n]
    
    def get_last_n_outcomes(self, trans_type = 'public', n=5):
        all_incomes = order_transactions(self.get_all_outcome(trans_type))
        return all_incomes[:n]
    
    def get_last_public_incomes (self, n=5):
        return self.get_last_n_incomes(trans_type = 'public', n = 5)
    
    def get_last_public_outcomes (self, n=5):
        return self.get_last_n_outcomes(trans_type = 'public', n = 5)
    
    def get_last_private_incomes (self, n=5):
        return self.get_last_n_incomes(trans_type = 'private', n = 5)
    
    def get_last_private_outcomes (self, n=5):
        return self.get_last_n_outcomes(trans_type = 'private', n = 5)
    
    def get_requested_income_or_outcome(self, type_of_trans, income):
        if income:
            output = self.get_all_income(trans_type=type_of_trans).\
                        aggregate(models.Sum('amount'))['amount__sum']
        else:
            output = self.get_all_outcome(trans_type=type_of_trans).\
                        aggregate(models.Sum('amount'))['amount__sum']
        if (str(output) == '') or (output is None):
            return 0.0 
        else:
            return float(output)
        
    
    def get_family_income_sum(self):
        return self.get_requested_income_or_outcome(type_of_trans='public', \
                                                    income=True)
        
    def get_family_outcome_sum(self):
        return self.get_requested_income_or_outcome(type_of_trans='public', \
                                                    income=False)
    
    def get_private_income_sum(self):
        return self.get_requested_income_or_outcome(type_of_trans='private', \
                                                    income=True)
        
    def get_private_outcome_sum(self):
        return \
            self.get_requested_income_or_outcome(type_of_trans='private', \
                                                 income=False)
            
    def get_private_balance(self):
        return round(self.get_private_income_sum() +\
               self.get_private_outcome_sum(), 2)
        
    def get_family_balance(self):
        return round(self.get_family_income_sum() +\
               self.get_family_outcome_sum(), 2)
               
    def order_all_family_transactions_by_date_desc(self):
        return self.order_all_family_transactions(\
                                                criterium = 'transactionstime',\
                                                descending = True)
    
    def order_all_family_transactions_by_date_asc(self):
        return self.order_all_family_transactions(\
                                                criterium = 'transactionstime',\
                                                descending = False)
    
    def order_all_family_transactions(self, criterium = 'transactionstime',\
                                                   descending = True):
        output = order_transactions(self.get_all_public_family_transactions(), \
                                    criterium, descending)
        return output
    
    def get_first_private_or_public_transact_datetime(self, public_transacts):
        if public_transacts:
            transactions = self.get_all_public_family_transactions()
        else:
            transactions = self.get_all_privat_user_transactions()
        min_date_time_db = transactions.aggregate(Min("transactionstime"))
        min_date_time = min_date_time_db['transactionstime__min']
        return min_date_time
    
    def get_first_transactions_datetime(self):
        return self.get_first_private_or_public_transact_datetime(\
                                                        public_transacts=True)
        
    def get_first_private_transactions_datetime(self):
        return self.get_first_private_or_public_transact_datetime(\
                                                        public_transacts=False)
        
    def get_user_settings(self):
        settings = UserSettings.objects.filter(user=self)
        return settings
    
    def get_settings_with_name(self):
        settings = self.get_user_settings()
        settings_as_voc = {}
        for current_setting in settings:
            for setting_name, _ in current_setting:
                settings_as_voc[setting_name] = current_setting
        return settings_as_voc 
    
    def get_user_settings_as_voc(self):
        settings = self.get_user_settings()
        settings_as_voc = {}
        for current_setting in settings:
            for setting_name, setting_value in current_setting:
                settings_as_voc[setting_name] = setting_value[1]
        return settings_as_voc   
        
class Currency(models.Model):
    short_name = models.CharField(max_length = 3, null=False, unique=True)
    full_name = models.CharField(max_length = 128, null = False)
    
    @classmethod
    def get_all_currencies_as_tuple(c):        
        all_currencies = c.objects.all()
        all_currencies_tuple = ()
        for cur_currency in all_currencies:
            currency_tuple = (cur_currency.short_name, cur_currency.full_name)
            all_currencies_tuple = all_currencies_tuple + (currency_tuple, )
        return all_currencies_tuple          

class ConfirmationData(models.Model):
    user = models.ForeignKey(Users)
    sentat = models.DateTimeField()
    code = models.CharField(max_length = 32)
    type = models.CharField(max_length = 255)
    is_expired = models.BooleanField(default=True)
    expiratin_date = models.DateTimeField()
    is_active = models.BooleanField(default = True)
    
    confirmation_email = 'email'
    confirmation_family = 'family'
    confirmation_password = 'password'
    confirmation_delete = 'delete'
    
class PublicTransaction(models.Model):
#     Class designed to store the information about each single 
#     transaction that are visible to all other family members
    
    user = models.ForeignKey(Users)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.ForeignKey(Currency, default=Currency.objects.get(pk=1))
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
    
    
class PrivatTransaction(models.Model):
#     Class designed to store the information about each single 
#     transaction that are visible only to originator
    
    user = models.ForeignKey(Users)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.ForeignKey(Currency, default=Currency.objects.get(pk=1))
    transactionstime = models.DateTimeField()
    purpose = models.CharField(max_length = 255)
    comment = models.CharField(max_length = 255, blank = True, null = True)
    deleted = models.BooleanField(default = False)
    
    def is_private(self):
        return True
    
    def is_public(self):
        return False
    
    def is_income(self):
        if self.amount >= 0:
            return True
        return False 
    
    def is_outcome(self):
        return not self.is_income()
    
    def get_user(self):
        return self.users.get_full_name()
    
    def __unicode__(self):
        return self.purpose+";"+str(self.amount)+";"\
            +str(self.transactionstime)
            
class Pseudonym(models.Model):
    pseudonym = models.CharField(max_length = 15)
    of_the_user = models.ForeignKey(Users, related_name="of_user")
    for_the_user = models.ForeignKey(Users, related_name="for_user")
    
    def __unicode__(self):
        return self.pseudonym  
    
class PreferncesTypes(models.Model):    
    prefernce_type = models.CharField(max_length = 6)    

class SitePreferncesList(models.Model):         
    setting_name = models.CharField(max_length = 255)
    
class SitePrefernce(models.Model):
    setting = models.ForeignKey(SitePreferncesList)
    type = models.ForeignKey(PreferncesTypes)    
    
class UserSettings(models.Model):
    user = models.ForeignKey(Users)
    setting = models.ForeignKey(SitePrefernce)
    value_bool = models.NullBooleanField(null = True)
    value_float = models.DecimalField(max_digits=5, decimal_places=4, null = True)
    value_string = models.CharField(max_length = 128, null=True)
    value_int = models.IntegerField(null=True)
    
#    default_tab_is_public = models.BooleanField(default = False, \
#                                                choices = default_tab)

    def __iter__(self):
        return self.get_property_value() 
        
    def get_property_value(self):
        setting_name = self.setting.setting.setting_name
        setting_type = self.setting.type.prefernce_type
        if setting_type == 'bool':
            setting_value = self.value_bool
        elif setting_type == 'float':
            setting_value = self.value_float
        elif setting_type == 'string':
            setting_value = self.value_string
        elif setting_type == 'int':
            setting_value = self.value_int
        else:
            setting_value = [self.value_bool, self.value_float, \
                             self.value_string, self.value_int]
        yield(setting_name, [setting_type, setting_value])