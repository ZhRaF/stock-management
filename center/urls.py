from django.urls import path
from . import views

urlpatterns=[
     path('dashboardCenter/<int:pk>/',views.dashcentre,name='dashboardCenter'),
]  