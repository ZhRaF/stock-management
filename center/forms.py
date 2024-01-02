from django.db.models import fields
from django import forms
from .models import Employe
from .models import ClientC


# Create your tests here.
class ClientCForm(forms.ModelForm):
    class Meta:
        model=ClientC
        fields=['nom_cl','prenom_cl','adresse_cl','telephone_cl','credit']
        labels = {
            
            'nom_cl' : 'Nom:',
            'prenom_cl':'Prenom:',
            'adresse_cl':'Adresse',
            'telephone_cl':'Téléphone',
            'credit':'credit',


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

