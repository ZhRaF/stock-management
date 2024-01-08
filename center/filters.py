import django_filters
from django_filters import DateFilter,CharFilter
from .models import VenteCentre
from django import forms

class VenteCentreFilter(django_filters.FilterSet):
    class Meta:
        model=VenteCentre
        fields=['type_Paiement_vc']
        labels = {
            
            'type_Paiement_vc':'Paiement:',
        }
    start_date=DateFilter(field_name='date_vc',lookup_expr='gte', label='Date début:', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date=DateFilter(field_name='date_vc',lookup_expr='lte', label='Date fin:', widget=forms.DateInput(attrs={'type': 'date'}))
    product_name=CharFilter(field_name='produit__designation_pc',lookup_expr='icontains',label='Produit:')
    client_name=CharFilter(field_name='client__nom_cl',lookup_expr='icontains',label='Client:')
 