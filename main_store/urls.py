from django.urls import path
from . import views



urlpatterns=[
    path('dashboard/',views.dash,name='dashboard'),
    
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
]