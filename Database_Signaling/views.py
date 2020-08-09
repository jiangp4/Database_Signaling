import os

from django.http.response import FileResponse, HttpResponse
from django.shortcuts import render
from Database_Signaling.settings import data_path


def send_file(request, f):
    f = os.path.join(data_path, f)
    
    if os.path.exists(f):
        return FileResponse(open(f, 'rb'))
    else:
        return render(request, 'error.html', {'message': 'File does not exist %s' % os.path.basename(f)})
    
    
def send_file_delete(request, f):
    f = os.path.join(data_path, f)
    
    if os.path.exists(f):
        fin = open(f)
        s = fin.read()
        fin.close()
        
        os.remove(f)
        
        response = HttpResponse(s, content_type="text/plain")
        response['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)
        return response
    else:
        return render(request, 'error.html', {'message': 'File does not exist %s' % os.path.basename(f)})

def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def download(request):
    return render(request, 'download.html')
