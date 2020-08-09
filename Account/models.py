from django.db import models

from django.contrib.auth.models import AbstractUser
from Database_Signaling.settings import MAX_STR_LENGTH

# Create your models here.
class Account(AbstractUser):
    # add additional fields in here
    email = models.EmailField('email')
    
    first_name = models.CharField('first_name', max_length = MAX_STR_LENGTH)
    last_name = models.CharField('last_name', max_length = MAX_STR_LENGTH)
    institute = models.CharField('institute', max_length = MAX_STR_LENGTH)
    
    birth_date = models.DateField('birth_date')
    
    url = models.URLField('url', blank=True)
    bio = models.TextField('bio', blank=True)
        
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'institute', 'birth_date']
    USERNAME_FIELD = 'username'
    
    def __str__(self): return self.username
