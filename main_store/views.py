from django.shortcuts import render,redirect
from django.db.models import Q
from .models import Produit
from .models import Fournisseur
from .models import Client
from .forms import ProduitForm
from .forms import FournisseurForm
from .forms import ClientForm
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
    return render(request,"main-store/dashboard/dashboard.html",)

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

    pdf_filename = 'Fournisseurs.pdf'

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
########fin produit ##########


######fournisseur##########
#liste des fournisseurs

def afficher_fournisseur(request):
    if 'q' in request.GET:
        q=request.GET['q']
        # fournisseurs=Fournisseur.objects.filter(nom_f__icontains=q)
        multiple_q=Q(Q(nom_f__icontains=q) | (Q(prenom_f__icontains=q)))
        fournisseurs=Fournisseur.objects.filter(multiple_q)
    else:
        fournisseurs=Fournisseur.objects.all()
    return render(request,"main-store/fournisseurs/FournisseurList.html",{"fournisseurs":fournisseurs})
#ajouter fournisseur
def ajouter_fournisseur(request):
    
    if request.method == "POST":          
        form=FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            fournisseur_name=form.cleaned_data.get('nom_f','prenom_f')
            messages.success(request,f'{fournisseur_name} a été ajouté')
            form = FournisseurForm()
            return render(request,"main-store/fournisseurs/fournisseurAdd.html",{"form":form})
    else:
        form = FournisseurForm()
        return render(request,"main-store/fournisseurs/fournisseurAdd.html",{"form":form,})

#modifier fournisseur
def modifier_fournisseur(request,pk):
    fournisseur=Fournisseur.objects.get(code_f=pk)
    if request.method=='POST':
        form=FournisseurForm(request.POST,instance=fournisseur)
        if form.is_valid():
            form.save()
            return redirect("fournisseurList")
    else:
        form=FournisseurForm(instance=fournisseur)
        return render(request,'main-store/fournisseurs/fournisseurEdit.html',{"form":form})
    
#suprimer fournisseur
def supprimer_fournisseur(request,pk):
    fournisseur=Fournisseur.objects.get(code_f=pk)   
    if request.method=='POST':           
            fournisseur.delete()       
            return redirect("fournisseurList")  
    else:          
        form=FournisseurForm(instance=fournisseur) 
        return render(request,'main-store/fournisseurs/fournisseurDelete.html',{"fournisseur":fournisseur})

#generation fichier PDF 
def imprimer_fournisseur(request):
    lignes = [["Code", "Nom","Prénom","Adresse","Télephone","Solde"]]  # Header row

    fournisseurs = Fournisseur.objects.all()

    for fournisseur in fournisseurs:
        ligne_fournisseur = [
            f"{fournisseur.code_f}",
            f"{fournisseur.nom_f}",
            f"{fournisseur.prenom_f}",
            f"{fournisseur.adresse_f}",
            f"{fournisseur.telephone_f }",
            f"{fournisseur.solde}",
        ]
        lignes.append(ligne_fournisseur)

    pdf_filename = 'Produits.pdf'

    # Create a PDF using ReportLab
    pdf_buffer = io.BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title at the top center
    title_style = styles['Title']
    title = Paragraph("Liste des fournisseurs", title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))  #

    # Current date on the right
    date_style = styles['Normal']
    current_date =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    date_paragraph = Paragraph(f"Date: {current_date}", date_style)
    elements.append(date_paragraph)
    elements.append(Spacer(1, 20))  

    col_widths = [50,100,100,100,100,100]
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
     
#######fin fournisseur#########


########client##########

#liste des client

def afficher_client(request):
    if 'q' in request.GET:
        q=request.GET['q']
        
        multiple_q=Q(Q(nom_cl__icontains=q) | (Q(prenom_cl__icontains=q)))
        clients=Client.objects.filter(multiple_q)
    else:
        clients=Client.objects.all()
    return render(request,"main-store/clients/clientList.html",{"clients":clients})
#ajouter client
def ajouter_client(request):
    
    if request.method == "POST":          
        form=ClientForm(request.POST)
                  
        if form.is_valid():
            form.save()
            client_name=form.cleaned_data.get('nom_cl','prenom_cl')
            messages.success(request,f'{client_name} a été ajouté')
            form = ClientForm()
            return render(request,"main-store/clients/clientAdd.html",{"form":form})
    else:
        form = ClientForm()
        return render(request,"main-store/clients/clientAdd.html",{"form":form,})

#modifier client
def modifier_client(request,pk):
    client=Client.objects.get(code_cl=pk)
    if request.method=='POST':
        form=ClientForm(request.POST,instance=client)
        if form.is_valid():
            form.save()
            return redirect("clientList")
    else:
        form=ClientForm(instance=client)
        return render(request,'main-store/clients/clientEdit.html',{"form":form})
    
#suprimer client
def supprimer_client(request,pk):
    client=Client.objects.get(code_cl=pk)   
    if request.method=='POST':           
            client.delete()       
            return redirect("clientList")  
    else:          
        form=ClientForm(instance=client) 
        return render(request,'main-store/clients/clientDelete.html',{"client":client})

#generation fichier PDF 
def imprimer_client(request):
    lignes = [["Code", "Nom","Prénom","Adresse","Télephone","Crédit"]]  # Header row

    clients = Client.objects.all()

    for client in clients:
        ligne_client= [
            f"{client.code_cl}",
            f"{client.nom_cl}",
            f"{client.prenom_cl}",
            f"{client.adresse_cl}",
            f"{client.telephone_cl }",
            f"{client.credit}",
        ]
        lignes.append(ligne_client)

    pdf_filename = 'Clients.pdf'

    # Create a PDF using ReportLab
    pdf_buffer = io.BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title at the top center
    title_style = styles['Title']
    title = Paragraph("Liste des clients", title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))  #

    # Current date on the right
    date_style = styles['Normal']
    current_date =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    date_paragraph = Paragraph(f"Date: {current_date}", date_style)
    elements.append(date_paragraph)
    elements.append(Spacer(1, 20))  

    col_widths = [50,100,100,100,100,100]
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
     
