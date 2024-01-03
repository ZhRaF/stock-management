from django.db import models

# Create your models here.

class Centre(models.Model):
    code_c = models.AutoField(primary_key=True)
    designation_c = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        # Check if the object is being created (not updated)
        if not self.pk:
            # Get the maximum existing code_c value or set to 0 if no records exist
            max_code_c = Centre.objects.aggregate(models.Max('code_c'))['code_c__max'] or 0
            self.code_c = max_code_c + 1

        super().save(*args, **kwargs)

class produits_centre(models.Model):
    Code_pc = models.AutoField(primary_key=True)
    designation_pc = models.CharField(max_length=50)
    centre = models.ForeignKey(Centre,on_delete=models.CASCADE)


class Employe(models.Model):
    code_e = models.AutoField(primary_key=True)
    nom_e = models.CharField(max_length=50)
    prenom_e = models.CharField(max_length=50)
    adresse_e = models.CharField(max_length=100)
    telephone_e = models.CharField(max_length=50)
    salaire_jour = models.FloatField(max_length=50,null=True, blank=True)
    centre = models.ForeignKey(Centre,on_delete=models.CASCADE)

class ClientC(models.Model):
    code_cl = models.AutoField(primary_key=True)
    nom_cl = models.CharField(max_length=50)
    prenom_cl = models.CharField(max_length=50)
    adresse_cl = models.CharField(max_length=100)
    telephone_cl = models.CharField(max_length=50)
    credit = models.FloatField(default=0.0)
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE, null=True)


from main_store.models import Client

class VenteCentre(models.Model):
    num_vc = models.AutoField(primary_key=True)
    qte_vc = models.IntegerField()
    date_vc = models.DateField()
    montant_vc = models.FloatField()   
    client = models.ForeignKey(ClientC,on_delete=models.CASCADE)
    produit = models.ForeignKey(produits_centre,on_delete=models.CASCADE)

    
