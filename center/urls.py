from django.urls import path
from . import views

urlpatterns=[
<<<<<<< HEAD
    path('dashboardCentre/',views.dashcentre,name='dashboardcentre'),

]
=======
     path('dashboardCenter/<int:pk>/',views.dashcentre,name='dashboardCenter'),
]  
>>>>>>> beb1fc4b562ff04ee68180aa4d12b6a5598b7bac
