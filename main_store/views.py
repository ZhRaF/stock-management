from django.shortcuts import render,redirect
from django.db.models import Q
from .models import Produit, Transfert, Vente
from .models import Fournisseur
from .models import Client
from .forms import Achat, AchatEditForm, Paiement_creditForm, ReglementForm, StockForm, TransfertForm, VenteEditForm, VenteForm
from .models import Client
from .models import Stock
from .forms import ProduitForm
from .forms import FournisseurForm
from .forms import ClientForm
from .forms import AchatForm
from .filters import AchatFilter, VenteFilter, stockFilter
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
from django.db.models import F, ExpressionWrapper, DecimalField, Sum


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

    pdf_filename = 'Fournisseurs.pdf'

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



#############achats#############
#liste des achat

def afficher_achat(request):
    
    achats = Achat.objects.all()
    myFilter = AchatFilter(request.GET, queryset=achats)

    
    achats = myFilter.qs

    achats = achats.annotate(
        montant_total=ExpressionWrapper(F('qte_a') * F('prix_unitaireHT'), output_field=DecimalField())
    )
    total_montant_total = achats.aggregate(total=Sum('montant_total'))['total']

    context={"achats":achats,'myFilter':myFilter,'total_montant_total': total_montant_total, }
    return render(request,"main-store/achats/achatList.html",context)

#ajouter achat

def ajouter_achat(request):
    
    if request.method == "POST":          
        form=AchatForm(request.POST)
                  
        if form.is_valid():
            form.save()
            cleaned_data = form.cleaned_data
            produit_name = cleaned_data['produit'].designationP  
            year_of_achat = cleaned_data['date_a'].year
            full_name=f"{produit_name}{year_of_achat}"
            qte_a = cleaned_data['qte_a']
            prix_unitaireHT = cleaned_data['prix_unitaireHT']
            montant_A = cleaned_data['montant_A']
            stock_exists = Stock.objects.filter(designation_s=full_name).exists()

            if stock_exists:
                
                stock_product = Stock.objects.get(designation_s=full_name)
                stock_product.qte_s += qte_a
                stock_product.save()
                success_message = f"Le produit {full_name} est déja en stock ."
                
            else:
                stock_product = Stock.objects.create(
                    designation_s=full_name,
                    qte_s=qte_a,
                    prix_achat=prix_unitaireHT
                )
                success_message = f"Le produit {full_name} est ajouté en stock ."
            
            

            stock_product.save()

            fournisseur_code= cleaned_data['fournisseur'].code_f
            fournisseur= Fournisseur.objects.get(code_f=fournisseur_code)
            fournisseur.solde+=(qte_a*prix_unitaireHT)-montant_A
            fournisseur.save()
            achat = form.save(commit=False)
            achat.stock=stock_product
            achat.save()
            
           
            messages.success(request, success_message)
            form = AchatForm()
            return render(request,"main-store/achats/achatAdd.html",{"form":form})
            
    else:
        form = AchatForm()
    return render(request,"main-store/achats/achatAdd.html",{"form":form,})

#######nouveau fournisseur
def achat_fournisseur(request):
    
    if request.method == "POST":          
        form=FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            form = FournisseurForm()
            return redirect('achatAdd')
    else:
        form = FournisseurForm()
        return render(request,"main-store/achats/achatFournisseur.html",{"form":form,})
##modifier achat
    
def modifier_achat(request,pk):
    achat=Achat.objects.get(num_a=pk)
    
    
    initial_montant=achat.montant_A
    if request.method=='POST':
        form=AchatEditForm(request.POST,instance=achat)
        if form.is_valid():
            cleaned_data = form.cleaned_data
           
            
            
            fournisseur=achat.fournisseur
           

            montant = cleaned_data['montant_A']   
           
            difference = montant - initial_montant
            if difference != 0:
                fournisseur.solde -= difference
                fournisseur.save()

                
            form.save()
            return redirect("achatList")
    else:
        form=AchatEditForm(instance=achat)
        return render(request,'main-store/achats/achatEdit.html',{"form":form})

##supprimer achat
def supprimer_achat(request,pk):
    achat=Achat.objects.get(num_a=pk)   
    if request.method=='POST':     
            fournisseur = achat.fournisseur
            qte_a = achat.qte_a
            prix_unitaireHT = achat.prix_unitaireHT
            montant_A = achat.montant_A
            if achat.type_Paiement_A=='Partiel':
                fournisseur.solde-=(qte_a*prix_unitaireHT)-montant_A
                fournisseur.save()
            stock=achat.stock
            if stock.qte_s <= 0 :
                stock.delete()
            else:
                stock.qte_s-=qte_a
                stock.save()
                if stock.qte_s <= 0:
                     stock.delete()

            achat.delete()       
            return redirect("achatList")  
    else:          
        return render(request,'main-store/achats/achatDelete.html',{"achat":achat})
    
##imprimer achat
def imprimer_achat(request):
    lignes = [["Numéro", "Date","Produit","Quantité","prix unitaire","fournisseur","Type paiement","Montant versé"]]  # Header row

    achats = Achat.objects.all()
    for achat in achats:
        ligne_achat= [
            f"{achat.num_a}",
            f"{achat.date_a}",
            f"{achat.produit}",
            f"{achat.qte_a}",
            f"{achat.prix_unitaireHT }",
            f"{achat.fournisseur}",
            f"{achat.type_Paiement_A}",
            f"{achat.montant_A}",
            
        ]
        lignes.append(ligne_achat)

    pdf_filename = 'Achats.pdf'

    # Create a PDF using ReportLab
    pdf_buffer = io.BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title at the top center
    title_style = styles['Title']
    title = Paragraph("Liste des achats", title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))  #

    # Current date on the right
    date_style = styles['Normal']
    current_date =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    date_paragraph = Paragraph(f"Date: {current_date}", date_style)
    elements.append(date_paragraph)
    elements.append(Spacer(1, 20))  

    col_widths = [50,80,80,50,70,100,80,80]
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
    
#############stock#############
#liste stock

def afficher_stock(request):
    
    stocks = Stock.objects.all()
    myFilter = stockFilter(request.GET, queryset=stocks)

    
    stocks = myFilter.qs

    stocks = stocks.annotate(
        montant_total=ExpressionWrapper(F('qte_s') * F('prix_achat'), output_field=DecimalField())
    )
    total_montant_total = stocks.aggregate(total=Sum('montant_total'))['total']

    context={"stocks":stocks,'myFilter':myFilter,'total_montant_total': total_montant_total, }
    return render(request,"main-store/stock/stockList.html",context)

##modifier stock
def modifier_stock(request,pk):
    stock=Stock.objects.get(num_s=pk)
    if request.method=='POST':
        form=StockForm(request.POST,instance=stock)
        if form.is_valid():
            form.save()
            return redirect("stockList")
    else:
        form=StockForm(instance=stock)
        return render(request,'main-store/stock/stockEdit.html',{"form":form})
#suprimer stock
def supprimer_stock(request,pk):
    stock=Stock.objects.get(num_s=pk)   
    if request.method=='POST':           
            stock.delete()       
            return redirect("stockList")  
    else:          
        return render(request,'main-store/stock/stockDelete.html',{"stock":stock})
##imprimer etat du stock

def imprimer_stock(request):
    lignes = [["Produit", "Quantité","Fournisseur","Dates d'achat","prix d'achat"]]  # Header row
    stocks = Stock.objects.all()
    for stock in stocks:
        achats = stock.achat.all() 
        
        fournisseurs = "\n".join([achat.fournisseur.nom_f for achat in achats])  
        dates = "\n".join([str(achat.date_a) for achat in achats])

        ligne_stock = [
        f"{stock.designation_s}",
        f"{stock.qte_s}",
        f"{fournisseurs}", 
        f"{dates}",
        f"{stock.prix_achat}"

        ]
        lignes.append(ligne_stock)

    pdf_filename = 'Stock.pdf'

    # Create a PDF using ReportLab
    pdf_buffer = io.BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title at the top center
    title_style = styles['Title']
    title = Paragraph("Etat du stock", title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))  #

    # Current date on the right
    date_style = styles['Normal']
    current_date =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    date_paragraph = Paragraph(f"Date: {current_date}", date_style)
    elements.append(date_paragraph)
    elements.append(Spacer(1, 20))  

    col_widths = [100,50,100,150,60]
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

#########ventes######
##afficher vente
def afficher_vente(request):
    
    ventes = Vente.objects.all()
    myFilter = VenteFilter(request.GET, queryset=ventes)

    
    ventes = myFilter.qs

    ventes = ventes.annotate(
        montant_total=ExpressionWrapper(F('qte_v') * F('prix_unitaireVT'), output_field=DecimalField())
    )
    total_montant_total = ventes.aggregate(total=Sum('montant_total'))['total']

    context={"ventes":ventes,'myFilter':myFilter,'total_montant_total': total_montant_total, }
    return render(request,"main-store/ventes/venteList.html",context)

#ajouter vente

def ajouter_vente(request):
    
    if request.method == "POST":          
        form=VenteForm(request.POST)
                  
        if form.is_valid():
            form.save()
            cleaned_data = form.cleaned_data
            produit_name = cleaned_data['stock'].designation_s  
            year_of_vente = cleaned_data['date_v'].year
            
            qte_v = cleaned_data['qte_v']
            prix_unitaireVT = cleaned_data['prix_unitaireVT']
            montant_v = cleaned_data['montant_v']
              
            stock_product = Stock.objects.get(designation_s=produit_name)
            stock_product.qte_s -= qte_v
            stock_product.save()
            if stock_product.qte_s<=0:
               
                success_message = f"Le produit {produit_name} est retiré du stock ."
            else :
                success_message = f"Le produit {produit_name}  est encore en stock ."
                
            
            
            

            stock_product.save()

            client_code= cleaned_data['client'].code_cl
            client= Client.objects.get(code_cl=client_code)
            client.credit+=(qte_v*prix_unitaireVT)-montant_v
            client.save()
            vente = form.save(commit=False)
            vente.save()
           
            
           
            messages.success(request, success_message)
            form = VenteForm()
            return render(request,"main-store/ventes/venteAdd.html",{"form":form})
            
    else:
        form = VenteForm()
    return render(request,"main-store/ventes/venteAdd.html",{"form":form,})
##modifier vente
    
def modifier_vente(request,pk):
    vente=Vente.objects.get(num_v=pk)
    
    
    initial_montant=vente.montant_v
    if request.method=='POST':
        form=VenteEditForm(request.POST,instance=vente)
        if form.is_valid():
            cleaned_data = form.cleaned_data
           
            
            
            client=vente.client
           

            montant = cleaned_data['montant_v']   
           
            difference = montant - initial_montant
            if difference != 0:
                client.credit -= difference
                client.save()

                
            form.save()
            return redirect("venteList")
    else:
        form=VenteEditForm(instance=vente)
        return render(request,'main-store/ventes/venteEdit.html',{"form":form})
##supprimer vente
def supprimer_vente(request,pk):
    vente=Vente.objects.get(num_v=pk)   
    if request.method=='POST':     
            client = vente.client
            qte_v = vente.qte_v
            prix_unitaireVT = vente.prix_unitaireVT
            montant_v = vente.montant_v
            if vente.type_Paiement_v=='Partiel':
                client.credit-=(qte_v*prix_unitaireVT)-montant_v
                client.save()
            stock=vente.stock
            
            
            stock.qte_s+=qte_v
            stock.save()
                
            vente.delete()
               
            return redirect("venteList")  
    else:          
        return render(request,'main-store/ventes/venteDelete.html',{"vente":vente})

##imprimer vente
def imprimer_vente(request):
    lignes = [["Numéro", "Date","Produit","Quantité","prix unitaire","client","Type paiement","Montant versé"]] 

    ventes = Vente.objects.all()
    for vente in ventes:
        ligne_vente= [
            f"{vente.num_v}",
            f"{vente.date_v}",
            f"{vente.stock}",
            f"{vente.qte_v}",
            f"{vente.prix_unitaireVT }",
            f"{vente.client}",
            f"{vente.type_Paiement_v}",
            f"{vente.montant_v}",
            
        ]
        lignes.append(ligne_vente)

    pdf_filename = 'Ventes.pdf'

    # Create a PDF using ReportLab
    pdf_buffer = io.BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title at the top center
    title_style = styles['Title']
    title = Paragraph("Liste des ventes", title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))  #

    # Current date on the right
    date_style = styles['Normal']
    current_date =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    date_paragraph = Paragraph(f"Date: {current_date}", date_style)
    elements.append(date_paragraph)
    elements.append(Spacer(1, 20))  

    col_widths = [50,80,80,50,70,100,80,80]
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

#liste fournisseurs non reglés
def fournisseur_non_regles(request):
    fournisseurs=Fournisseur.objects.filter(solde__gt=0)
    if 'q' in request.GET:
        q=request.GET['q']
        multiple_q=Q(Q(nom_f__icontains=q) | (Q(prenom_f__icontains=q)))
        fournisseurs=fournisseurs.filter(multiple_q)
    return render(request,"main-store/fournisseurs/fournisseurListNonSettled.html",{"fournisseurs":fournisseurs})

def regler_fournisseur(request, pk):
    fournisseur = Fournisseur.objects.get(code_f=pk)
    fullname = f"{fournisseur.nom_f} {fournisseur.prenom_f}"

    if request.method == 'POST':
        form = ReglementForm(fournisseur, request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            montant = cleaned_data.get('montant_r')
            if fournisseur.solde >= montant:
                fournisseur.solde -= montant
                fournisseur.save()

                reglement = form.save(commit=False)  # Create Reglement instance but NOT save to the database yet
                reglement.fournisseur = fournisseur  # Set the fournisseur attribute
                reglement.save()  # Save the Reglement instance

                return redirect('fournisseurSettleList')
    else:
        form = ReglementForm(fournisseur)

    return render(request, "main-store/fournisseurs/fournisseurSettle.html", {"form": form, "solde": fournisseur.solde, "name": fullname})


def imprimer_fournisseurNonRegles(request):
    lignes = [["Code", "Nom", "Prénom", "Adresse", "Télephone", "Solde"]]  # Header row

    fournisseurs = Fournisseur.objects.exclude(solde=0)

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

    pdf_filename = 'FournisseursNonRegles.pdf'

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

#liste clients non reglés
def client_non_regles(request):
    clients=Client.objects.filter(credit__gt=0)
    if 'q' in request.GET:
        q=request.GET['q']
        multiple_q=Q(Q(nom_cl__icontains=q) | (Q(prenom_cl__icontains=q)))
        clients=clients.filter(multiple_q)
    return render(request,"main-store/clients/clientListNonSettled.html",{"clients":clients})
#regler client

def regler_client(request, pk):
    client = Client.objects.get(code_cl=pk)
    fullname = f"{client.nom_cl} {client.prenom_cl}"

    if request.method == 'POST':
        form = Paiement_creditForm(client, request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            montant = cleaned_data.get('montant_cl')
            if client.credit >= montant:
                client.credit -= montant
                client.save()

                Paiement_credit = form.save(commit=False)  # Create Paiement_credit instance but NOT save to the database yet
                Paiement_credit.client = client  # Set the client attribute
                Paiement_credit.save()  # Save the Paiement_credit instance

                return redirect('clientSettleList')
    else:
        form = Paiement_creditForm(client)

    return render(request, "main-store/clients/clientSettle.html", {"form": form, "credit": client.credit, "name": fullname})

#imprimer liste clients non reglés

def imprimer_clientNonRegles(request):
    lignes = [["Code", "Nom", "Prénom", "Adresse", "credit"]]  # Header row

    clients = Client.objects.exclude(credit=0)

    for client in clients:
        ligne_client = [
            f"{client.code_cl}",
            f"{client.nom_cl}",
            f"{client.prenom_cl}",
            f"{client.adresse_cl}",
            f"{client.telephone_cl }",
            f"{client.credit}",
        ]
        lignes.append(ligne_client)

    pdf_clilename = 'clientsNonRegles.pdf'

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
    response['Content-Disposition'] = f'attachment; filename="{pdf_clilename}"'

    return response

#afficher transfert

def afficher_transfert(request):
    transferts = Transfert.objects.all()

    if 'q' in request.GET:
        q = request.GET['q']
        transferts = transferts.filter(num_t__icontains=q)

    return render(request, "main-store/transfert/transfertList.html", {"transferts": transferts})





#ajouter transfert
from center.models import produits_centre

from django.core.exceptions import ObjectDoesNotExist

def ajouter_transfert(request):
    if request.method == "POST":          
        form = TransfertForm(request.POST)
        if form.is_valid():
            stock = form.cleaned_data['produit']

            try:
                # Try to get the existing_prdCentre
                existing_prdCentre = produits_centre.objects.get(centre=form.cleaned_data['centre'], designation_pc=stock)

                # If produit exists, update the quantity
                existing_prdCentre.qte_pc += form.cleaned_data['qte_t']
                existing_prdCentre.save()
            except produits_centre.DoesNotExist:
                # If produit doesn't exist, add it to the center
                produit = produits_centre()
                produit.designation_pc = stock
                produit.qte_pc = form.cleaned_data['qte_t']
                produit.centre = form.cleaned_data['centre']
                produit.save()

            # stock maj
            stock.qte_s -= form.cleaned_data['qte_t']
            stock.save()

            # montant totale de transfert
            montant_t = stock.prix_achat * form.cleaned_data['qte_t'] 
            form.instance.montant_t = montant_t
            form.save()  

            form = TransfertForm()
            transferts = Transfert.objects.all()
            return render(request, "main-store/transfert/transfertList.html", {"form": form, "transferts": transferts})
        else:
            # form is not valid, stay in the form + display errors
            return render(request, "main-store/transfert/transfertAdd.html", {"form": form})
    else:
        form = TransfertForm()
        return render(request, "main-store/transfert/transfertAdd.html", {"form": form})


def supprimer_transfert(request, pk):
    transfert = Transfert.objects.get(num_t=pk)

    if request.method == 'POST':
        prdCentre = produits_centre.objects.get(
            centre=transfert.centre.code_c,
            designation_pc=transfert.produit.designation_s
        )
        prdCentre.qte_pc -= transfert.qte_t

        # Check if the quantity in prdCentre is zero, delete the object
        if prdCentre.qte_pc == 0:
            prdCentre.delete()
        else:
            prdCentre.save()

        stock = Stock.objects.get(num_s=transfert.produit.num_s)
        stock.qte_s += transfert.qte_t
        stock.save()

        transfert.delete()
        return redirect('transfertList')
    else:
        return render(request, "main-store/transfert/transfertDelete.html", {"transfert": transfert})
