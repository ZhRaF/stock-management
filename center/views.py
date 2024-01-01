from django.shortcuts import render

# Create your views here.
<<<<<<< HEAD
def dashcentre(request):
    return render(request,"dashboard/baseCenter.html",)

=======

#dashboard
def dashcentre(request,pk):
    return render(request,"center/dashboard/dashboardCenter.html",)  
>>>>>>> beb1fc4b562ff04ee68180aa4d12b6a5598b7bac
