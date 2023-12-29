from django.shortcuts import render

# Create your views here.
def dash(request):
    return render(request,"dashboard/baseStore.html",)

def dashcentre(request):
    return render(request,"dashboard/baseCenter.html",)