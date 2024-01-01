from django.urls import path
from . import views

urlpatterns=[
    path('dashboardCentre/',views.dashcentre,name='dashboardcentre'),

]
