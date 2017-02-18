from django.shortcuts import render
from test_data.forms.form_create_test_users import CreateTestUsersForm
from budget.models import Users


# Create your views here.

def start_page_old(request):    
    return render(request, "budget/test_data/create_users.html")

def start_page(request, user_form = None):
    if user_form == None:
        user_form = CreateTestUsersForm()  
    
    return render(request, "budget/test_data/create_users.html", \
                  {'form':user_form})

def select_test_user(request):
    all_users = Users.objects.all()
    necessary_user_info = [[user.get_full_name(), user.pk] for user in all_users]
    return render(request, "budget/test_data/select_test_user.html", \
                 {'all_users':necessary_user_info})