from django.shortcuts import render
from django.db.models import Q, Func, F
from Association.models import Gene, AliasName, Signal, Association
from Database_Signaling.settings import FLOAT_PRECISION, MAX_ENTRY_COUNT

def search_gene(gene):
    gene_lst = Gene.objects.filter(Symbol=gene)
    if len(gene_lst) > 0: return gene_lst
    
    alias_lst = AliasName.objects.filter(name=gene)
    if len(alias_lst) > 0:
        genes = set()
        for alias in alias_lst:
            genes.update(alias.gene_set.all())
        return genes
    
    return None


def search_signal(signal):
    
    signal_lst = Signal.objects.filter(ID=signal)
    if len(signal_lst) > 0: return signal_lst
    
    signal_lst = Signal.objects.filter(Gene__Symbol=signal)
    if len(signal_lst) > 0: return signal_lst
    
    signal_lst = Signal.objects.filter(Gene__Alias__name=signal)
    if len(signal_lst) > 0: return signal_lst
    
    signal_lst = Signal.objects.filter(Q(ID__icontains=signal))
    if len(signal_lst) > 0: return signal_lst
    
    return None




# Create your views here.
def search(request):
    if not request.user.is_authenticated:
        return render(request, 'error.html', {'message': 'User not login.'})
    
    query = select_signal = select_gene = None
    
    format_string = '%.' + str(FLOAT_PRECISION) + 'f'
    
    # analyze available signals
    if 'query_input' in request.POST:
        query = request.POST['query_input']
        
        if not query:
            return render(request, 'error.html', {'message': 'Please enter a search term.', 'GOBACK': 5})
    
    elif 'select' in request.GET:
        select = request.GET['select']
        max_count = float(request.GET['max_count'])
        
        stype, select = select.split('_', 1)
        
        if stype == 'signal':
            select_signal = select
        
        elif stype == 'gene':
            select_gene = select
        
        else:
            return render(request, 'error.html', {'message': 'Unknown select type %s.' % stype, 'GOBACK': 5})
    
    # go to next step by input signals
    if query:
        signal_lst = search_signal(query)
        gene_lst = search_gene(query)
        
        # still possible for empty signal by no data collected
        if signal_lst is not None:
            lst = []
            
            for signal in signal_lst:
                # only include signals with some associations
                associations = Association.objects.filter(treatment__signal=signal)
                if associations.count() > 0: lst.append(signal)
            
            if len(lst) > 0:
                signal_lst = lst
            else:
                signal_lst = None
        
        
        if signal_lst is None and gene_lst is None:
            return render(request, 'error.html',
                          {'message': 'Cannot find any results with your query %s.' % query, 'GOBACK': 5})
        
        return render(request, 'search_results.html',
                      {'signal_lst': signal_lst,
                       'gene_lst': gene_lst,
                       'query': query,
                       'max_count': MAX_ENTRY_COUNT,
                       })
    
    elif select_signal or select_gene:
        
        if select_signal:
            signal = Signal.objects.get(ID=select_signal)
            associations = Association.objects.filter(treatment__signal=signal)
            target = 'Gene'
        else:
            associations = Association.objects.filter(gene__Symbol=select_gene)
            target = 'Signal'
        
        if associations.count() > max_count:
            associations = associations.annotate(abs_value=Func(F('value_adj'), function='ABS')).order_by('-abs_value')
            associations = associations[:max_count]
        
        for assocation in associations:
            assocation.value = format_string % assocation.value
            assocation.value_adj = format_string % assocation.value_adj
        
        
        return render(request, 'associations.html', {
            'associations': associations,
            'target': target,
            'float_precision': FLOAT_PRECISION,
            })
    
    
    else:
        return render(request, 'search.html', {'signals': [v.ID for v in Signal.objects.all()]})
