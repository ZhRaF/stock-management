from django.db import models



# Create your models here.

class Fournisseur(models.Model):
    code_f = models.AutoField(primary_key=True)
    nom_f = models.CharField(max_length=50)
    prenom_f = models.CharField(max_length=50)
    adresse_f = models.CharField(max_length=100)
    telephone_f = models.CharField(max_length=50)
    solde = models.FloatField(default=0.0)
    def __str__(self):
        return f"{self.nom_f} {self.prenom_f}"

class Reglement(models.Model):
    num_r = models.AutoField(primary_key=True)
    date_r = models.DateField()
    montant_r = models.FloatField()
    fournisseur= models.ForeignKey(Fournisseur,on_delete=models.CASCADE)

class Stock(models.Model):
    num_s = models.AutoField(primary_key=True)
    designation_s = models.CharField(max_length=50)
    qte_s = models.IntegerField(null=True,default=0)
    prix_achat = models.FloatField(null=True,default=0)
    def __str__(self):
        return self.designation_s

class Produit(models.Model):
    code_P = models.AutoField(primary_key=True)
    designationP = models.CharField(max_length=50)
    def __str__(self):
        return self.designationP

class Achat(models.Model):
    num_a = models.AutoField(primary_key=True)
    qte_a = models.IntegerField()
    date_a = models.DateField()
    type_choices=[
         ('Entier', 'Entier'),
        ('Partiel', 'Partiel'),
    ]
    type_Paiement_A = models.CharField(max_length=20,choices=type_choices)
    montant_A = models.FloatField()
    prix_unitaireHT = models.FloatField()
    fournisseur= models.ForeignKey(Fournisseur, on_delete = models.CASCADE)
    stock = models.ForeignKey(Stock ,on_delete = models.CASCADE, null=True, default=None)
    produit = models.ForeignKey(Produit ,on_delete = models.CASCADE)


class Client(models.Model):
    code_cl = models.AutoField(primary_key=True)
    nom_cl = models.CharField(max_length=50)
    prenom_cl = models.CharField(max_length=50)
    adresse_cl = models.CharField(max_length=100)
    telephone_cl = models.CharField(max_length=50)
    credit = models.FloatField(default=0.0)


class Paiement_credit(models.Model):
    num_pc = models.AutoField(primary_key=True)
    date_pc = models.DateField()
    montant_cl = models.FloatField()
    Client = models.ForeignKey(Client ,on_delete = models.CASCADE)
    

class Vente(models.Model):
    num_v = models.AutoField(primary_key=True)
    qte_v = models.IntegerField()
    date_v = models.DateField()
    type_choices=[
         ('Entier', 'Entier'),
        ('Partiel', 'Partiel'),
    ]
    type_paiement_v = models.CharField(max_length=20,choices=type_choices,default='Entier')
    montant_v = models.FloatField()
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit,on_delete=models.CASCADE)
from center.models import Centre

class Transfert(models.Model):
    num_t= models.AutoField(primary_key=True)
    qte_t = models.IntegerField()
    date_t= models.DateField()
    produit = models.ForeignKey(Stock,on_delete=models.CASCADE)
    centre = models.ForeignKey(Centre,on_delete=models.CASCADE)
    montant_t = models.FloatField()
