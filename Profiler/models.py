from Database_Signaling.settings import MAX_UPLOAD_SIZE

from django.db import models
from django.core.exceptions import ValidationError

def file_size(value):
    if value.size > MAX_UPLOAD_SIZE * 1024 * 1024:
        raise ValidationError('File size should not exceed %d MiB. Please download and run locally for huge input.' % MAX_UPLOAD_SIZE)

# Create your models here.
class TaskUpload(models.Model):
    #title = models.CharField('title', max_length=MAX_STR_LENGTH)
    task_file = models.FileField('task_file', upload_to='upload/', validators=[file_size])
    
    def __unicode__(self): return "%s" % self.task_file
    def __str__(self): return self.__unicode__()
