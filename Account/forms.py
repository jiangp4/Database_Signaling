from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Account
from django.forms.widgets import TextInput


class AccountCreateForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('username', 'first_name', 'last_name', 'email', 'birth_date', 'institute', 'url', 'bio')

#class AccountAuthenticationForm(AuthenticationForm):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.fields['username'].widget.attrs.update({'autocomplete': 'off'})
#        self.fields['password'].widget.attrs.update({'autocomplete': 'off'})

class AccountUpdateForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email', 'birth_date', 'institute', 'url', 'bio')
    
        widgets = {
            **{
                'username' : TextInput(attrs={'readonly': 'readonly'}),
               },
        }
