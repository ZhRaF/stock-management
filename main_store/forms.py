from django.db.models import fields
from django import forms
from .models import Produit 
from .models import Client 
from .models import Fournisseur
class ProduitForm(forms.ModelForm):
    class Meta:
        model=Produit
        fields=['designationP']
        labels = {
            'designationP': 'Désignation:'
        }

class FournisseurForm(forms.ModelForm):
    class Meta:
        model=Fournisseur
        fields=['nom_f','prenom_f','adresse_f','telephone_f']
        labels = {
            
            'nom_f' : 'Nom:',
            'prenom_f':'Prenom:',
            'adresse_f':'Adresse',
            'telephone_f':'Téléphone',

        }

class ClientForm(forms.ModelForm):
    class Meta:
        model=Client
        fields=['nom_cl','prenom_cl','adresse_cl','telephone_cl']
        labels = {
            
            'nom_cl' : 'Nom:',
            'prenom_cl':'Prenom:',
            'adresse_cl':'Adresse',
            'telephone_cl':'Téléphone',

        }