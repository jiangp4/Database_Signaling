from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    #path('login/', views.AccountLoginView.as_view(), name="login"),
    path('account_create/', views.AccountCreateView.as_view(), name='account_create'),
    path('account_update/', views.AccountUpdateView.as_view(), name='account_update'),
    path('account_update_complete/', views.account_update_complete, name='account_update_compete'),
    path('account_detail/<str:username>/', views.AccountDetailView.as_view(), name='account_detail'),
    
    path('password/', RedirectView.as_view(url='/accounts/password_reset/'), name='password_reset'),
]
