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


    path('clientList/',views.afficher_client,name='clientList'),
    path('clientAdd/',views.ajouter_client,name='clientAdd'),
    path('clientEdit/<int:pk>/',views.modifier_client,name='clientEdit'),
    path('clientDelete/<int:pk>/',views.supprimer_client,name='clientDelete'),
    path('clientPrint',views.imprimer_client,name='clientPrint'),

    path('achatList/',views.afficher_achat,name='achatList'),
    path('achatAdd/',views.ajouter_achat,name='achatAdd'),
    path('achatFournisseur/',views.achat_fournisseur,name='achatFournisseur'),
    path('achatDelete/<int:pk>/',views.supprimer_achat,name='achatDelete'),
    path('achatEdit/<int:pk>/',views.modifier_achat,name='achatEdit'),
    path('achatPrint',views.imprimer_achat,name='achatPrint'),

    path('stockList/',views.afficher_stock,name='stockList'),
    path('stockEdit/<int:pk>/',views.modifier_stock,name='stockEdit'),
    path('stockDelete/<int:pk>/',views.supprimer_stock,name='stockDelete'),
    path('stockPrint',views.imprimer_stock,name='stockPrint'),

    path('venteList/',views.afficher_vente,name='venteList'),
    path('venteAdd/',views.ajouter_vente,name='venteAdd'),
    path('ventePrint',views.imprimer_vente,name='ventePrint'),
    path('venteDelete/<int:pk>/',views.supprimer_vente,name='venteDelete'),
    path('venteEdit/<int:pk>/',views.modifier_vente,name='venteEdit'),

      
]