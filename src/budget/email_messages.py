'''
Created on Jun 24, 2014

@author: thavr
'''

def get_body_email_conf(username, email, url):
    
    output_message = "Dear " + username + "!\n\nWe are happy that you decided" + \
                     " to join us and use our product. In order to extend " + \
                     "the ways our product can support you we ask you to" + \
                     " confirm your email " + email + ". Otherwise not all " + \
                     "features will be available for you. For example we " + \
                     "won't be able to recover your password.\n\n" + \
                     "You can confirm your email address simply by clicking "+\
                     "on the link below:\n\n<a href = \"" + url + "\">" + \
                     "Confirm email</a>\n\nThank you. \n\nAdministration"

    
    return  output_message
            
def get_body_family_conf(name, email, url):
    return "Dear " + name + ". \n\nUser with email " + email + \
                " has showed desire to join your family. Note that by" + \
                " allowing it you will automatically grant access for this " + \
                "user to see and change all public transactions of other " + \
                "members of your family including yours. Be responsible." + \
                " Do not add people from households other than yours or the" + \
                " people you do not know personally." + \
                "\n\nIn order to grant access to the user click this link: " + \
                "\n\n<a href = \"" + url + "\">I do know this user and " + \
                "I explicitly allow him to have access to public family " + \
                "transactions</a>\n\nOtherwise just ignore this " + \
                "email. Link will be valid for 1 month. Than it will " + \
                "expire.\n\nBest Regards\n\nAdministration"
