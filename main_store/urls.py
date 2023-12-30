from django.urls import path
from . import views



urlpatterns=[
    path('dashboard/',views.dash,name='dashboard'),
    path('dashboardCentre/',views.dashcentre,name='dashboardcentre'),
     path('productList/',views.afficher_produits,name='productList'),
      path('productAdd/',views.ajouter_produits,name='productAdd'),
    path('productEdit/<int:pk>/',views.modifier_produit,name='productEdit'),
    path('productDelete/<int:pk>/',views.supprimer_produit,name='productDelete'),
     path('productPrint',views.imprimer_produit,name='productPrint'),
]