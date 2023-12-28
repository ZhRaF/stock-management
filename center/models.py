from django.db import models

# Create your models here.




# Create your models here.

class Centre(models.Model):
    Code_c = models.AutoField(primary_key=True)
    designation_c = models.CharField()

class produits_centre(models.Model):
    Code_pc = models.AutoField(primary_key=True)
    designation_pc = models.CharField()
    centre = models.ForeignKey(Centre,on_delete=models.CASCADE)


class Employe(models.Model):
    code_e = models.AutoField(primary_key=True)
    nom_e = models.CharField(max_length=50)
    prenom_e = models.CharField(max_length=50)
    adresse_e = models.CharField(max_length=100)
    telephone_e = models.CharField(max_length=50)
    salaire_jour = models.FloatField(max_length=50)
    centre = models.ForeignKey(Centre,on_delete=models.CASCADE)


class VenteCentre(models.Model):
    num_vc = models.AutoField(primary_key=True)
    qte_vc = models.IntegerField()
    date_vc = models.DateField()
    montant_vc = models.FloatField()   
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    produit = models.ForeignKey(produits_centre,on_delete=models.CASCADE)

    