from django.db.models import fields
from django import forms
from .models import Produit, Stock 
from .models import Client 
from .models import Fournisseur
from .models import Achat


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
            'adresse_f':'Adresse:',
            'telephone_f':'Téléphone:',

        }

class ClientForm(forms.ModelForm):
    class Meta:
        model=Client
        fields=['nom_cl','prenom_cl','adresse_cl','telephone_cl']
        labels = {
            
            'nom_cl' : 'Nom:',
            'prenom_cl':'Prenom:',
            'adresse_cl':'Adresse:',
            'telephone_cl':'Téléphone:',

        }

class AchatForm(forms.ModelForm):
  
    class Meta:
        model=Achat
        
        fields=['date_a','produit','qte_a','prix_unitaireHT','fournisseur','type_Paiement_A','montant_A']
        labels = {
            
            'date_a':'Date:',
            'produit':'Produit:',
            'qte_a':'Quantité',
            'prix_unitaireHT':'Prix Unitaire:',
            'fournisseur':'Fournisseur:',
            'type_Paiement_A':'Paiement:',
            'montant_A':'Montant versé:',


        }
    
        widgets = {
            'date_a': forms.DateInput(attrs={'type': 'date'}),  


        }


    def clean(self):
        cleaned_data = super().clean()
        qte_a = cleaned_data.get('qte_a')
        prix_unitaireHT = cleaned_data.get('prix_unitaireHT')
        montant_A = cleaned_data.get('montant_A')
        type_Paiement_A = cleaned_data.get('type_Paiement_A')

        if type_Paiement_A == 'Partiel' and (montant_A is None or montant_A >=qte_a * prix_unitaireHT):
            raise forms.ValidationError("Le montant versé doit être inférieur au montant total")

        return cleaned_data
    def clean_montant_A(self):
        montant_A = self.cleaned_data.get('montant_A')
        qte_a = self.cleaned_data.get('qte_a')
        prix_unitaireHT = self.cleaned_data.get('prix_unitaireHT')
        type_Paiement_A = self.cleaned_data.get('type_Paiement_A')

        if montant_A is None or montant_A == '':
            if type_Paiement_A == 'Entier':
                montant_A = qte_a * prix_unitaireHT

        return montant_A


class StockForm(forms.ModelForm):
    class Meta:
        model=Stock
        fields=['prix_achat','qte_s']
        labels = {
            
            'prix_achat' : 'Prix d achat:',
            'qte_s':'Quantité:',
            

        }