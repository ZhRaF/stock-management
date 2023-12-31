from django.shortcuts import render,redirect
from .models import Produit
from .forms import ProduitForm
from django.contrib import messages
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Table
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.platypus import Paragraph
import datetime
from reportlab.platypus import Spacer


# Create your views here.


#affichage dashboard
def dash(request):
    return render(request,"dashboard/dashboard.html",)

#########Produit###########
#liste des produits
def afficher_produits(request):
    if 'q' in request.GET:
        q=request.GET['q']
        produits=Produit.objects.filter(designationP__icontains=q)
    else:
        produits=Produit.objects.all()
    return render(request,"main-store/produits/productList.html",{"products":produits})


#ajouter produit
def ajouter_produits(request):
    
    if request.method == "POST":          
        form=ProduitForm(request.POST)
                  
        if form.is_valid():
            form.save()
            product_name=form.cleaned_data.get('designationP')
            messages.success(request,f'{product_name} a été ajouté')
            form = ProduitForm()
            return render(request,"main-store/produits/productAdd.html",{"form":form})
    else:
        form = ProduitForm()
        return render(request,"main-store/produits/productAdd.html",{"form":form,})

#modifier produit
def modifier_produit(request,pk):
    produit=Produit.objects.get(code_P=pk)
    if request.method=='POST':
        form=ProduitForm(request.POST,instance=produit)
        if form.is_valid():
            form.save()
            return redirect("productList")
    else:
        form=ProduitForm(instance=produit)
        return render(request,'main-store/produits/productEdit.html',{"form":form})
    
#suprimer produit
def supprimer_produit(request,pk):
    produit=Produit.objects.get(code_P=pk)   
    if request.method=='POST':           
            produit.delete()       
            return redirect("productList")  
    else:          
        form=ProduitForm(instance=produit) 
        return render(request,'main-store/produits/productDelete.html',{"product":produit})

#generation fichier PDF 
def imprimer_produit(request):
    lignes = [["Code", "Designation"]]  # Header row

    produits = Produit.objects.all()

    for produit in produits:
        ligne_produit = [
            f"{produit.code_P}",
            f"{produit.designationP}",
        ]
        lignes.append(ligne_produit)

    pdf_filename = 'Produits.pdf'

    # Create a PDF using ReportLab
    pdf_buffer = io.BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title at the top center
    title_style = styles['Title']
    title = Paragraph("Liste des produits", title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))  #

    # Current date on the right
    date_style = styles['Normal']
    current_date =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    date_paragraph = Paragraph(f"Date: {current_date}", date_style)
    elements.append(date_paragraph)
    elements.append(Spacer(1, 20))  

    col_widths = [150, 300]
    table_style = [
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#95c089')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),  # Left padding for cells
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),  # Right padding for cells
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),  # Add box/borders around the table
    ]

    table = Table(lignes, style=table_style, colWidths=col_widths)
    elements.append(table)
    pdf.build(elements)

    # Prepare the response
    pdf_buffer.seek(0)
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'

    return response

     
