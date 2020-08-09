from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from Account.forms import AccountCreateForm, AccountUpdateForm
from Account.models import Account

#class AccountLoginView(LoginView):
#    form_class = AccountAuthenticationForm
#    success_url = reverse_lazy('index')
#    template_name = 'registration/login.html'


class AccountCreateView(generic.CreateView):
    form_class = AccountCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/account_create.html'


class AccountUpdateView(generic.UpdateView):
    form_class = AccountUpdateForm
    success_url = reverse_lazy('account_update_compete')
    template_name = 'registration/account_update.html'
    
    def get_object(self):
        return get_object_or_404(Account, pk=self.request.user.id)


class AccountDetailView(generic.DetailView):
    model = Account
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    template_name = 'registration/account_detail.html'



def account_update_complete(request):
    return render(request, 'registration/account_update_complete.html')

def account_information(request, username):
    curator = Account.objects.get(username=username)
    
    return render(request, 'registration/account_information.html', {'user': curator})
