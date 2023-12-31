from django.db.models import fields
from django import forms
from .models import Produit 

class ProduitForm(forms.ModelForm):
    class Meta:
        model=Produit
        fields=['designationP']
        labels = {
            'designationP': 'Désignation:'
        }