import os, pandas
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from .forms import TaskUploadForm
from .models import TaskUpload
from Profiler.util import ridge_significance_test
from Database_Signaling.settings import RIDGE_ALPHA, data_path, MAX_SAMPLE_COUNT, MAX_UPLOAD_SIZE, FLOAT_PRECISION, NRAND

# Create your views here.
class TaskUploadView(generic.CreateView):
    form_class = TaskUploadForm
    template_name = 'task_upload.html'
    
    def get_success_url(self):
        return reverse_lazy('task_run', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['max_sample_count'] = MAX_SAMPLE_COUNT
        context['max_upload_size'] = MAX_UPLOAD_SIZE
        return context



def task_run(request, pk):
    task_upload = TaskUpload.objects.get(pk=pk)
    f = task_upload.task_file.path
    
    signature = pandas.read_csv(os.path.join(data_path, 'diff.centroid'), sep='\t')
    
    try:
        file_type = f.split('.').pop().lower()
        
        if file_type == 'csv':
            response = pandas.read_csv(f, index_col=0)
        
        elif file_type in ['xls', 'xlsx']:
            response = pandas.read_excel(f, index_col=0)
        
        else:
            response = pandas.read_csv(f, sep='\t', index_col=0)
    
    except:
        task_upload.delete()
        os.remove(f)
        
        return render(request, 'error.html', {'message': 'Fail reading matrix %s. Please check the format of your input.' % os.path.basename(f)})
    
    if response.shape[1] > MAX_SAMPLE_COUNT:
        task_upload.delete()
        os.remove(f)
        
        return render(request, 'error.html', {'message': 'Number of samples %d exceeds allowance %d. Please download our software to run locally.' % (response.shape[1], MAX_SAMPLE_COUNT)})
    
    
    # Input quality check
    if response.isnull().sum().sum() > 0:
        task_upload.delete()
        os.remove(f)
        
        return render(request, 'error.html', {'message': 'Null values detected in the input. Please do missing value imputation first.'})
    
    if response.index.value_counts().max() > 1:
        response = response.groupby(response.index).median()
    
    try:
        beta, se, zscore, pvalue = ridge_significance_test(signature, response, RIDGE_ALPHA, "two-sided", NRAND)
    except:
        task_upload.delete()
        os.remove(f)
        
        return render(request, 'error.html', {'message': 'Regression failure.'})
    
    task_upload.delete()
    os.remove(f)
    
    result_lst = []
    
    
    format_string_regular = '%.' + str(FLOAT_PRECISION) + 'f'
    format_string_scientific = '%.' + str(FLOAT_PRECISION) + 'e'
    
    
    for title in beta:
        result = pandas.concat([beta[title], se[title], zscore[title], pvalue[title]], axis=1, join='inner')
        result.columns = ['Coef', 'StdErr', 'Zscore', 'Pvalue']
        
        result.sort_values('Pvalue', inplace=True, ascending=True)
        
        for v in ['Zscore']:
            result.loc[:, v] = result.loc[:, v].apply(lambda v: format_string_regular % v)
        
        for v in ['Coef', 'StdErr', 'Pvalue']:
            result.loc[:, v] = result.loc[:, v].apply(lambda v: format_string_scientific % v)
        
        result_lst.append([title, result])
    
    return render(request, 'task_run.html', {'result_lst': result_lst})
