from django.db.models import fields
from django import forms
from .models import Employe, VenteCentre, produits_centre
from .models import ClientC


# Create your tests here.
class ClientCForm(forms.ModelForm):
    class Meta:
        model=ClientC
        fields=['nom_cl','prenom_cl','adresse_cl','telephone_cl']
        labels = {
            
            'nom_cl' : 'Nom:',
            'prenom_cl':'Prenom:',
            'adresse_cl':'Adresse',
            'telephone_cl':'Téléphone',
            


        }

class EmployeForm(forms.ModelForm):
    class Meta:
        model=Employe
        fields=['nom_e','prenom_e','adresse_e','telephone_e',]
        labels = {
            
            'nom_e' : 'Nom:',
            'prenom_e':'Prenom:',
            'adresse_e':'Adresse',
            'telephone_e':'Téléphone',

        }
class VenteCentreForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        centre_instance = kwargs.pop('centre', None)
        super(VenteCentreForm, self).__init__(*args, **kwargs)
        
        if centre_instance:
            self.fields['client'].queryset = ClientC.objects.filter(centre=centre_instance)
            self.fields['produit'].queryset = produits_centre.objects.filter(centre=centre_instance)
    class Meta:
        model=VenteCentre
        
        fields=['date_vc','produit','qte_vc','prix_unitaireVTC','client','type_Paiement_vc','montant_vc']
        labels = {
            
            'date_vc':'Date:',
            'produit':'Produit:',
            'qte_vc':'Quantité',
            'prix_unitaireVTC':'Prix Unitaire:',
            'client':'Client:',
            'type_Paiement_vc':'Paiement:',
            'montant_vc':'Montant versé:',


        }
    
        widgets = {
            'date_vc': forms.DateInput(attrs={'type': 'date'}),  


        }


    def clean(self):
        cleaned_data = super().clean()
        qte_vc = cleaned_data.get('qte_vc')
        prix_unitaireVTC = cleaned_data.get('prix_unitaireVTC')
        montant_vc = cleaned_data.get('montant_vc')
        type_Paiement_vc = cleaned_data.get('type_Paiement_vc')

        if type_Paiement_vc == 'Partiel' and (montant_vc is None or montant_vc >=qte_vc * prix_unitaireVTC):
            raise forms.ValidationError("Le montant versé doit être inférieur au montant total")

        return cleaned_data
    def clean_montant_vc(self):
        montant_vc = self.cleaned_data.get('montant_vc')
        qte_vc = self.cleaned_data.get('qte_vc')
        prix_unitaireVTC = self.cleaned_data.get('prix_unitaireVTC')
        type_Paiement_vc = self.cleaned_data.get('type_Paiement_vc')

        if montant_vc is None or montant_vc == '':
            if type_Paiement_vc == 'Entier':
                montant_v = qte_vc * prix_unitaireVTC

        return montant_vc
class VenteCentreEditForm(forms.ModelForm):
  
    class Meta:
        model=VenteCentre
        
        fields=['type_Paiement_vc','montant_vc']
        labels = {
            
            
            
            'type_Paiement_vc':'Paiement:',
            'montant_vc':'Montant versé:',


        }

