import os, sys, pandas
from django.core.management.base import BaseCommand#, CommandError
from Association.models import AliasName, Gene, Signal, Treatment, Association


class Command(BaseCommand):
    help = 'Build the database data from command line'
    
    def add_arguments(self, parser):
        parser.add_argument('operation', nargs='+', type=str)
    
    def handle(self, *args, **options):
        operation = options['operation'][0]
        
        if operation == 'insert_gene':
            self.insert_gene()
        
        elif operation == 'insert_signal':
            self.insert_signal()
        
        elif operation == 'insert_treatment':
            self.insert_treatment()
        
        elif operation == 'insert_correlation':
            self.insert_correlation()
        
        else:
            sys.stderr.write('Cannot recognize operation %s\n' % operation)
    
    
    def insert_treatment(self):
        Immune_Path = os.path.join(os.getenv("HOME"), 'workspace', 'Data', 'Cancer', 'Immune')
        
        lst_association = []
        
        included = set()
        
        info_map = os.path.join(Immune_Path, 'Signaling', 'Output', 'diff.merge.info')
        info_map = pandas.read_csv(info_map, sep='\t', index_col=0)
        
        # nan values should be jump empty strings
        info_map.fillna('', inplace=True)
        
        # use gene map to reduce MySQL communications
        gene_map = {}
        
        # 
        for signal_type in ['Cytokine', 'Chemokine', 'Growth_Factor', 'Inhibitory']:
            print('processing', signal_type)
            
            data = pandas.read_csv(os.path.join(Immune_Path, signal_type, 'Output', 'diff.merge.gz'), sep='\t', index_col=0)
            
            assert data.columns.value_counts().max() == 1
            assert data.index.value_counts().max() == 1
            
            # adjust to standard deviation
            data_adj = data/data.std()
            
            count = 0
            
            for ID in data.columns:
                print('%.2f' % (100.0 * count / data.shape[1]), '%')
                count += 1
                
                if ID not in info_map.index:
                    sys.stderr.write('Cannot find meta information for %s\n' % ID)
                    continue
                
                signal, condition, duration, dose = info_map.loc[ID]
                
                dataset = ID.split('@')[-1]
                
                # jump duplications
                if signal_type == 'Growth_Factor' and signal in ['TGFB1', 'TGFB2', 'TGFB3']: continue
                
                if ID in included:
                    sys.stderr.write('Duplicated %s\n' % ID)
                    continue
                else:
                    included.add(ID)
                
                dataset, platform, platform_detail = dataset.split('.', 2)
                
                if platform == 'RNASeq':
                    assert platform_detail.find('_GRCh38') > 0
                    platform_detail = ''
                
                signal = Signal.objects.get(ID=signal)
                
                rc_treatment = Treatment.objects.filter(ID=ID)
            
                if rc_treatment.count() == 0:
                    rc_treatment = Treatment.objects.create(
                        ID=ID,
                        signal=signal,
                        condition = condition,
                        duration=duration,
                        dose=dose,
                        dataset=dataset,
                        platform=platform,
                        platform_detail=platform_detail
                        )
                else:
                    assert rc_treatment.count() == 1
                    rc_treatment = rc_treatment[0]
                        
                arr = data[ID].dropna()
                included = set()
                
                for symbol, v in arr.iteritems():
                    #if symbol not in ['DGCR5', 'FAM49A', 'FAM49B', 'WDR66', 'WDR63', 'WDR60', 'WDR34']: continue
                    
                    rc_gene = gene_map.get(symbol)
                    
                    if rc_gene is None:
                        rc_gene = Gene.objects.filter(Symbol=symbol)
                        
                        if rc_gene.count() == 0:
                            rc_gene = Gene.objects.filter(Alias__name=symbol)
                        
                        if rc_gene.count() == 0:
                            sys.stderr.write('Cannot find %s\n' % symbol)
                            continue
                        
                        elif rc_gene.count() > 1:
                            sys.stderr.write('Ambiguous %s\n' % symbol)
                            continue
                        
                        gene_map[symbol] = rc_gene = rc_gene[0]
                    
                    
                    # translated alias will duplicate existing gene names
                    if rc_gene.Symbol in included:
                        sys.stderr.write('Conflict alias translation %s %s\n' % (symbol, rc_gene.Symbol))
                        continue
                    
                    lst_association.append(
                        Association(
                            treatment=rc_treatment,
                            gene=rc_gene,
                            value=v,
                            value_adj=data_adj.loc[symbol, ID]
                        )
                    )
                    
                    included.add(rc_gene.Symbol)
        
                # please first TRUNCATE TABLE Association_association
                Association.objects.bulk_create(lst_association)
                del lst_association[:]
    

    def insert_correlation(self):
        Immune_Path = os.path.join(os.getenv("HOME"), 'workspace', 'Data', 'Cancer', 'Immune')
        
        included = os.path.join(Immune_Path, 'Signaling', 'Output', 'diff.merge.filter.gz')
        included = pandas.read_csv(included, sep='\t', index_col=0).columns
        
        info_map = os.path.join(Immune_Path, 'Signaling', 'Output', 'diff.merge.info')
        info_map = pandas.read_csv(info_map, sep='\t', index_col=0)
        
        Treatment.objects.all().update(flag_correlation=False)
    
        for ID in included:
            if ID not in info_map.index:
                sys.stderr.write('Cannot find meta information for %s\n' % ID)
                continue
            
            rc_treatment = Treatment.objects.get(ID=ID)
            rc_treatment.flag_correlation = True
            rc_treatment.save()
    
    
    def insert_signal(self):
        Immune_Path = os.path.join(os.getenv("HOME"), 'workspace', 'Data', 'Cancer', 'Immune')
        
        for signal_type in ['Cytokine', 'Chemokine', 'Growth_Factor', 'Inhibitory']:
            log = os.path.join(Immune_Path, signal_type, 'log', 'Receptor_' + signal_type + '.xlsx')
            
            xls = pandas.ExcelFile(log, engine='openpyxl')
            for family in xls.sheet_names:
                data = xls.parse(family, index_col=0)['Gene']
                data = data.loc[~data.index.isnull()]
                
                for ID, lst in data.iteritems():
                    if lst is None or len(lst) == 0: continue
                    
                    rc_signal = Signal.objects.filter(ID=ID)
            
                    if rc_signal.count() == 0:
                        rc_signal = Signal.objects.create(ID=ID)
                    else:
                        assert rc_signal.count() == 1
                        rc_signal = rc_signal[0]
                    
                    lst = lst.replace('+', ',').split(',')
                    lst = set([v.strip() for v in lst])
                    
                    for gid in lst:
                        genes = Gene.objects.filter(Symbol=gid)
                        
                        if genes.count() == 0:
                            sys.stderr.write('Cannot find gene symbol %s\n' % gid)
                            continue
                        else:
                            assert genes.count() == 1
                            rc_signal.Gene.add(genes[0])
            
            xls.close()
    
    
    
    def insert_gene(self):
        cnt_genes = cnt_alias = cnt_previous = 0
        
        gene_info = os.path.join(os.getenv("HOME"), 'workspace', 'Data', 'GeneInfo', 'NCBI', 'gene_info.9606')
        
        fin = open(gene_info)
        
        for l in fin:
            fields = l.rstrip('\n').split('\t')
            
            symbol = fields[2].strip()
            alias = fields[4].strip()
            
            if len(symbol) == 0: continue
            
            rc_gene = Gene.objects.filter(Symbol=symbol)
            
            if rc_gene.count() == 0:
                rc_gene = Gene.objects.create(Symbol=symbol)
                cnt_genes += 1
            else:
                assert rc_gene.count() == 1
                rc_gene = rc_gene[0]
                cnt_previous += 1
            
            # insert all alias if there is any
            if len(alias) == 0: continue
            
            alias_lst = alias.split('|')
            
            for alias in alias_lst:
                if len(alias) == 0: continue
                
                rc_alias = AliasName.objects.filter(name=alias)
                
                if rc_alias.count() == 0:
                    rc_alias = AliasName.objects.create(name=alias)
                    cnt_alias = cnt_alias + 1
                else:
                    assert rc_alias.count() == 1
                    rc_alias = rc_alias[0]
                
                rc_gene.Alias.add(rc_alias)
        
        fin.close()
        
        print(cnt_genes, 'created genes', cnt_previous, 'previous genes', cnt_alias, 'alias')
