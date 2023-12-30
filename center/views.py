from django.shortcuts import render

# Create your views here.

#dashboard
def dashcentre(request,pk):
    return render(request,"center/dashboard/dashboardCenter.html",)  