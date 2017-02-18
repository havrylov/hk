'''
Created on Aug 20, 2014

@author: thavr
'''

from django import forms
from budget.models import Currency

class EditPreferncesForm(forms.Form):
    default_tab = (('pub', 'Public Tab'),
                   ('priv', 'Private Tab'))
    currencies = Currency.get_all_currencies_as_tuple()

    start_tab = forms.EmailField(label="Select start Tab ", \
                             widget=forms.Select(choices=default_tab))
    curr = forms.CharField(label="Select main currency ", \
                             widget=forms.Select(choices=currencies))
#     class Meta:
#         model = UserSettings
#         default_tab = ((True, 'Public Tab'), 
#                    (False, 'Private Tab'))
#         fields = ['default_tab_is_public']
#         widgets = {
#             'default_tab_is_public': forms.Select(choices = default_tab),
#         }
