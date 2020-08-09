from django.contrib import admin
from Profiler.models import TaskUpload

# Register your models here.
class TaskUploadAdmin(admin.ModelAdmin):
    list_display = ('task_file',)
    ordering = ('task_file',)
    search_fields = ('task_file',)

admin.site.register(TaskUpload, TaskUploadAdmin)
