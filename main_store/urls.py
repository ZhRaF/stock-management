from django.urls import path
from . import views



urlpatterns=[
    
    path('',views.dash,name='dashboard'),
     path('productList/',views.afficher_produits,name='productList'),
      path('productAdd/',views.ajouter_produits,name='productAdd'),
    path('productEdit/<int:pk>/',views.modifier_produit,name='productEdit'),
    path('productDelete/<int:pk>/',views.supprimer_produit,name='productDelete'),
     path('productPrint',views.imprimer_produit,name='productPrint'),

     path('fournisseurList/',views.afficher_fournisseur,name='fournisseurList'),
      path('fournisseurAdd/',views.ajouter_fournisseur,name='fournisseurAdd'),
    path('fournisseurEdit/<int:pk>/',views.modifier_fournisseur,name='fournisseurEdit'),
    path('fournisseurDelete/<int:pk>/',views.supprimer_fournisseur,name='fournisseurDelete'),
     path('fournisseurPrint',views.imprimer_fournisseur,name='fournisseurPrint'),
      path('fournisseurListNonSettled/',views.fournisseur_non_regles,name='fournisseurSettleList'),
      path('fournisseurSettle/<int:pk>/',views.regler_fournisseur,name='fournisseurSettle'),
      path('fournisseurPrintNonSettled',views.imprimer_fournisseurNonRegles,name='fournisseurPrintNonSettled'),


      path('clientList/',views.afficher_client,name='clientList'),
      path('clientAdd/',views.ajouter_client,name='clientAdd'),
    path('clientEdit/<int:pk>/',views.modifier_client,name='clientEdit'),
    path('clientDelete/<int:pk>/',views.supprimer_client,name='clientDelete'),
     path('clientPrint',views.imprimer_client,name='clientPrint'),
     path('clientListNonSettled/',views.client_non_regles,name='clientSettleList'),
      path('clientSettle/<int:pk>/',views.regler_client,name='clientSettle'),
      path('clientPrintNonSettled',views.imprimer_clientNonRegles,name='clientPrintNonSettled'),


      path('achatList/',views.afficher_achat,name='achatList'),
      path('achatAdd/',views.ajouter_achat,name='achatAdd'),
       path('achatFournisseur/',views.achat_fournisseur,name='achatFournisseur'),
       path('achatDelete/<int:pk>/',views.supprimer_achat,name='achatDelete'),
    

       path('stockList/',views.afficher_stock,name='stockList'),
       path('stockEdit/<int:pk>/',views.modifier_stock,name='stockEdit'),
       path('stockDelete/<int:pk>/',views.supprimer_stock,name='stockDelete'),
   
        path('transfertAdd/',views.ajouter_transfert,name='transfertAdd'),
        path('transfertList/',views.afficher_transfert,name='transfertList'),
        path('transfertDelete/<int:pk>/',views.supprimer_transfert,name='transfertDelete'),

      
]