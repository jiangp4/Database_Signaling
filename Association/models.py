from django.db import models
from Database_Signaling.settings import MAX_CHAR_LENGTH


class AliasName(models.Model):
    name = models.CharField(max_length=MAX_CHAR_LENGTH, primary_key = True)
        
    def __unicode__(self): return self.name
    def __str__(self): return self.__unicode__()


class Gene(models.Model):
    Symbol = models.CharField(max_length=MAX_CHAR_LENGTH, primary_key = True)
    
    # use for searching
    Alias = models.ManyToManyField(AliasName)
    
    def __unicode__(self): return self.Symbol
    def __str__(self): return self.__unicode__()


class Signal(models.Model):
    ID = models.CharField(max_length=MAX_CHAR_LENGTH, primary_key = True)
    
    Gene = models.ManyToManyField(Gene)
    
    def __unicode__(self): return self.ID
    def __str__(self): return self.__unicode__()



class Treatment(models.Model):
    ID = models.CharField(max_length=MAX_CHAR_LENGTH, primary_key=True)
    
    signal = models.ForeignKey(Signal, related_name='association', on_delete=models.CASCADE)
    
    #signal_detail = models.CharField(max_length=MAX_CHAR_LENGTH, default='')
    
    condition = models.CharField(max_length=MAX_CHAR_LENGTH, default='')
    
    duration = models.CharField(max_length=MAX_CHAR_LENGTH, default='')
    dose = models.CharField(max_length=MAX_CHAR_LENGTH, default='')
    
    dataset = models.CharField(max_length=MAX_CHAR_LENGTH, default='')
    platform = models.CharField(max_length=MAX_CHAR_LENGTH, default='')
    platform_detail = models.CharField(max_length=MAX_CHAR_LENGTH, default='')
    
    flag_correlation = models.BooleanField(default=False)
    
    def __unicode__(self): return "%s" % self.ID
    def __str__(self): return self.__unicode__()



class Association(models.Model):
    treatment = models.ForeignKey(Treatment, related_name='association', on_delete=models.CASCADE)
    gene = models.ForeignKey(Gene, related_name='association', on_delete=models.CASCADE)
    
    value = models.FloatField()
    value_adj = models.FloatField()
    
    class Meta:
        unique_together = (('treatment', 'gene'),)
    
    def __unicode__(self): return u'%s_%s %.2e' % (self.treatment, self.gene, self.value)
