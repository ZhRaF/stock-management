from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Centre, Fournisseur, Reglement, Stock, Produit, Achat, Client, Paiement_credit, Vente, Transfert

# Register your models here
admin.site.register(Centre)
admin.site.register(Fournisseur)
admin.site.register(Reglement)
admin.site.register(Stock)
admin.site.register(Produit)
admin.site.register(Achat)
admin.site.register(Client)
admin.site.register(Paiement_credit)
admin.site.register(Vente)
admin.site.register(Transfert)
