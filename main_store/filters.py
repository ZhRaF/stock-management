import django_filters
from django_filters import DateFilter,CharFilter
from .models import Achat
from .models import Stock
from django import forms

class AchatFilter(django_filters.FilterSet):
    class Meta:
        model=Achat
        fields=['type_Paiement_A']
        labels = {
            
            'type_Paiement_A':'Paiement:',
        }
    start_date=DateFilter(field_name='date_a',lookup_expr='gte', label='Date début:', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date=DateFilter(field_name='date_a',lookup_expr='lte', label='Date fin:', widget=forms.DateInput(attrs={'type': 'date'}))
    product_name=CharFilter(field_name='produit__designationP',lookup_expr='icontains',label='Produit:')
    fournisseur_name=CharFilter(field_name='fournisseur__nom_f',lookup_expr='icontains',label='Fournisseur:')
 
class stockFilter(django_filters.FilterSet):
    class Meta:
        model=Stock
        exclude = ['designation_s']
        
    start_date=DateFilter(field_name='achat__date_a',lookup_expr='gte', label='Date début:', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date=DateFilter(field_name='achat__date_a',lookup_expr='lte', label='Date fin:', widget=forms.DateInput(attrs={'type': 'date'}))
    fournisseur=CharFilter(field_name='achat__fournisseur__nom_f',lookup_expr='icontains',label='Produit:')
    designation_s=CharFilter(field_name='designation_s',lookup_expr='icontains',label='Produit:')
