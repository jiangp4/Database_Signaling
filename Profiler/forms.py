from django.forms import ModelForm
from Profiler.models import TaskUpload

class TaskUploadForm(ModelForm):
    class Meta:
        model = TaskUpload
        fields = ('task_file',)
