from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import produits_centre, Employe, VenteCentre

# Register your models here

admin.site.register(produits_centre)
admin.site.register(Employe)
admin.site.register(VenteCentre)
