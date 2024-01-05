from django.urls import path
from . import views

urlpatterns=[
    path('dashboardCenter/<int:centre>/',views.dashcentre,name='dashboardCenter'),
    path('employeList/<int:centre>/',views.afficher_employes,name='employeList'),
    path('employeAdd/<int:centre>/',views.ajouter_employe,name='employeAdd'),
    path('employeEdit/<int:pk>/<int:centre>/',views.modifier_employe,name='employeEdit'),
    path('employeDelete/<int:pk>/<int:centre>/',views.supprimer_employe,name='employeDelete'),
    path('employePrint/<int:centre>/',views.imprimer_employes,name='employePrint'),

    path('dashboardCenter/<int:centre>/',views.dashcentre,name='dashboardCenter'),
    path('clientList/<int:centre>/',views.afficher_clients,name='clientList'),
    path('clientAdd/<int:centre>/',views.ajouter_client,name='clientAdd'),
    path('clientEdit/<int:pk>/<int:centre>/',views.modifier_client,name='clientEdit'),
    path('clientDelete/<int:pk>/<int:centre>/',views.supprimer_client,name='clientDelete'),
    path('clientPrint/<int:centre>/',views.imprimer_clients,name='clientPrint'),

    path('produitCentreList/<int:centre>/',views.afficher_produit_centre,name='produitCentreList'),
    path('produitCentrePrint/<int:centre>/',views.imprimer_produit_centre,name='produitCentrePrint'),



]  
