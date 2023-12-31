from django.shortcuts import render

# Create your views here.
def dashcentre(request):
    return render(request,"dashboard/baseCenter.html",)

