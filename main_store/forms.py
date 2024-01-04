from django.db.models import fields
from django import forms
from .models import Produit, Stock, Vente 
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

class AchatEditForm(forms.ModelForm):
  
    class Meta:
        model=Achat
        
        fields=['type_Paiement_A','montant_A']
        labels = {
            
            
            
            'type_Paiement_A':'Paiement:',
            'montant_A':'Montant versé:',


        }
    
class StockForm(forms.ModelForm):
    class Meta:
        model=Stock
        fields=['prix_achat','qte_s']
        labels = {
            
            'prix_achat' : 'Prix d achat:',
            'qte_s':'Quantité:',
            

        }


class VenteForm(forms.ModelForm):
  
    class Meta:
        model=Vente
        
        fields=['date_v','stock','qte_v','prix_unitaireVT','client','type_Paiement_v','montant_v']
        labels = {
            
            'date_v':'Date:',
            'stock':'Produit:',
            'qte_v':'Quantité',
            'prix_unitaireVT':'Prix Unitaire:',
            'client':'Client:',
            'type_Paiement_v':'Paiement:',
            'montant_v':'Montant versé:',


        }
    
        widgets = {
            'date_v': forms.DateInput(attrs={'type': 'date'}),  


        }


    def clean(self):
        cleaned_data = super().clean()
        qte_v = cleaned_data.get('qte_v')
        prix_unitaireVT = cleaned_data.get('prix_unitaireVT')
        montant_v = cleaned_data.get('montant_v')
        type_Paiement_v = cleaned_data.get('type_Paiement_v')

        if type_Paiement_v == 'Partiel' and (montant_v is None or montant_v >=qte_v * prix_unitaireVT):
            raise forms.ValidationError("Le montant versé doit être inférieur au montant total")

        return cleaned_data
    def clean_montant_v(self):
        montant_v = self.cleaned_data.get('montant_v')
        qte_v = self.cleaned_data.get('qte_v')
        prix_unitaireVT = self.cleaned_data.get('prix_unitaireVT')
        type_Paiement_v = self.cleaned_data.get('type_Paiement_v')

        if montant_v is None or montant_v == '':
            if type_Paiement_v == 'Entier':
                montant_v = qte_v * prix_unitaireVT

        return montant_v
class VenteEditForm(forms.ModelForm):
  
    class Meta:
        model=Vente
        
        fields=['type_Paiement_v','montant_v']
        labels = {
            
            
            
            'type_Paiement_v':'Paiement:',
            'montant_v':'Montant versé:',


        }