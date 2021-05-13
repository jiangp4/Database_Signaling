from django.contrib import admin

from .models import AliasName, Gene, Signal
from Association.models import Treatment, Association


class AliasNameAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ['name',]
    search_fields = ('name',)

admin.site.register(AliasName, AliasNameAdmin)


class GeneAdmin(admin.ModelAdmin):
    ordering = ('Symbol',)
    list_display = ['Symbol', 'get_alias']
    search_fields = ('Symbol', 'Alias__name')
    
    def get_alias(self, obj):
        return ' | '.join([p.name for p in obj.Alias.all()])

admin.site.register(Gene, GeneAdmin)


class SignalAdmin(admin.ModelAdmin):
    ordering = ('ID',)
    list_display = ['ID', 'get_gene']
    search_fields = ('ID', 'Gene__ID', 'Gene__Symbol', 'Gene__Alias__name')
    
    def get_gene(self, obj):
        return ' | '.join([p.Symbol for p in obj.Gene.all()])
    
admin.site.register(Signal, SignalAdmin)


class TreatmentAdmin(admin.ModelAdmin):
    ordering = ('ID',)
    list_display = ['ID', 'signal', 'condition', 'duration', 'dose', 'dataset', 'platform', 'platform_detail', 'flag_correlation']
    search_fields = ('ID', 'signal', 'condition', 'duration', 'dose', 'dataset', 'platform', 'platform_detail', 'flag_correlation')

admin.site.register(Treatment, TreatmentAdmin)


class AssociationAdmin(admin.ModelAdmin):
    ordering = ('treatment', 'gene')
    list_display = ['treatment', 'gene', 'value', 'value_adj']
    search_fields = ('treatment', 'gene')

admin.site.register(Association, AssociationAdmin)
