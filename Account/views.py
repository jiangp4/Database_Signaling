from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from Account.forms import AccountCreateForm, AccountUpdateForm
from Account.models import Account

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

#class AccountLoginView(LoginView):
#    form_class = AccountAuthenticationForm
#    success_url = reverse_lazy('index')
#    template_name = 'registration/login.html'


class AccountCreateView(generic.CreateView):
    form_class = AccountCreateForm
    success_url = reverse_lazy('account_create_compete')
    template_name = 'registration/account_create.html'

    def form_valid(self, form):
        
        if self.request.is_secure():
            http = 'https'
        else:
            http = 'http'
        
        current_site = '%s://%s' % (http, self.request.META['HTTP_HOST'])
        
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        
        mail_subject = 'Activate your account.'
        
        message = render_to_string('registration/activate_email.html',
            {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                #'token': default_token_generator.make_token(user),
            },
        )
        
        to_email = form.cleaned_data.get('email')
        
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.content_subtype = "html"
        email.send()
        
        return super(AccountCreateView, self).form_valid(form)


def activate(request, uidb64):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    #  and default_token_generator.check_token(user, token)
    if user is not None:
        user.is_active = True
        user.save()
        
        return render(request, 'complete.html', {'title': 'User account create complete', 'description': 'Thank you for your email confirmation. Now you can login your account.'})

    else:
        return render(request, 'error.html', {'message': 'Activation link is invalid!'})



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


def agreement(request):
    return render(request, 'registration/agreement.html')

def account_create_complete(request):
    return render(request, 'complete.html', {'title': 'User account create complete', 'description': 'Please check your email and confirm the registration.'})


def account_update_complete(request):
    return render(request, 'complete.html', {'title': 'User account update complete', 'description': 'Successful user information change of %s' % request.user.username})


def account_information(request, username):
    curator = Account.objects.get(username=username)
    
    return render(request, 'registration/account_information.html', {'user': curator})
