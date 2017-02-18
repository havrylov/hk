'''
Created on May 25, 2014

@author: thavr
'''

from budget.create_user import user_creation_procedure
from django.http import HttpRequest
from random import seed, randint
import django


def generate_random_email(length_addr = 4, length_dom = 4):
    
    seed()
    email = ""
    for _ in range(length_addr):
        email += chr(randint(97,122))
        
    email += '@'
    for _ in range(length_dom):
        email += chr(randint(97,122))
    email += '.com'
    return email

def create_user (email,password,family_email="",birthdate="",cellcountry="",\
                 cellarea='',cellnumber='',addrcountry='',addrpostid='',\
                 addrcity='',addrstr='',addrhousenum='',addrapt='',\
                 addradditional='',fname='',sname=''):
    request = HttpRequest()
    request.POST["email"] = email
    request.POST['password'] = password
    request.POST['family_email'] = family_email
    request.POST['birthdate'] = birthdate
    request.POST['cellcountry'] = cellcountry
    request.POST['cellarea'] = cellarea
    request.POST['cellnumber'] = cellnumber
    request.POST['addrcountry'] = addrcountry
    request.POST['addrpostid'] = addrpostid
    request.POST['addrcity'] = addrcity
    request.POST['addrstr'] = addrstr
    request.POST['addrhousenum'] = addrhousenum
    request.POST['addrapt'] = addrapt
    request.POST['addradditional'] = addradditional
    request.POST['fname'] = fname
    request.POST['sname'] = sname
    
    uu = user_creation_procedure(request)
    return uu




if __name__ == '__main__':
    django.setup()
    email = generate_random_email()
    uu = create_user(email, "12345678")
    print uu
    email2=generate_random_email()
    fam_member = create_user(email2, "12345678", family_email = email, \
                             fname = "Abanga", sname="Maksimov")
    print fam_member