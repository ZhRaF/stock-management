from django.db import models
from center.models import Centre
# Create your models here.

class Fournisseur(models.Model):
    code_f = models.AutoField(primary_key=True)
    nom_f = models.CharField(max_length=50)
    prenom_f = models.CharField(max_length=50)
    adresse_f = models.CharField(max_length=100)
    telephone_f = models.CharField(max_length=50)
    solde = models.FloatField()

class Reglement(models.Model):
    num_r = models.AutoField(primary_key=True)
    date_r = models.DateField()
    montant_r = models.FloatField()
    fournisseur= models.ForeignKey(Fournisseur,on_delete=models.CASCADE)

class Stock(models.Model):
    num_s = models.AutoField(primary_key=True)
    designation_s = models.CharField()
    qte_s = models.IntegerField()
    prix_achat = models.FloatField()


class Produit(models.Model):
    code_P = models.AutoField(primary_key=True)
    designationP = models.CharField()

class Achat(models.Model):
    num_a = models.AutoField(primary_key=True)
    qte_a = models.IntegerField()
    date_a = models.DateField()
    type_Paiement_A = models.CharField()
    montant_A = models.FloatField()
    prix_unitaireHT = models.FloatField()
    fournisseur= models.ForeignKey(Fournisseur, on_delete = models.CASCADE)
    stock = models.ForeignKey(Stock ,on_delete = models.CASCADE)
    produit = models.ForeignKey(Produit ,on_delete = models.CASCADE)

class Client(models.Model):
    code_cl = models.AutoField(primary_key=True)
    nom_cl = models.CharField(max_length=50)
    prenom_cl = models.CharField(max_length=50)
    adresse_cl = models.CharField(max_length=100)
    telephone_cl = models.CharField(max_length=50)
    credit = models.FloatField()

class Paiement_credit(models.Model):
    num_pc = models.AutoField(primary_key=True)
    date_pc = models.DateField()
    montant_cl = models.FloatField()
    Client = models.ForeignKey(Client ,on_delete = models.CASCADE)
    

class Vente(models.Model):
    num_v = models.AutoField(primary_key=True)
    qte_v = models.IntegerField()
    date_v = models.DateField()
    type_paiement_v = models.CharField()
    montant_v = models.FloatField()
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit,on_delete=models.CASCADE)
    #last field not sure depending on the product model

class Transfert(models.Model):
    quantiteT = models.IntegerField()
    dateT= models.DateField()
    produit = models.ForeignKey(Produit,on_delete=models.CASCADE)
    centre = models.ForeignKey(Centre,on_delete=models.CASCADE)

