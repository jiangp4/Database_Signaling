from django.urls import path
from . import views

urlpatterns = [
    path('task_upload/', views.TaskUploadView.as_view(), name='task_upload'),
    path('task_run/<int:pk>/', views.task_run, name='task_run'),
]
