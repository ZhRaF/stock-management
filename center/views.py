from django.shortcuts import render,redirect
from django.db.models import Q
from .models import ClientC, Employe, VenteCentre, produits_centre
from .models import Centre
from .models import ClientC as Client
from .forms import EmployeForm, VenteCentreEditForm, VenteCentreForm
from .forms import ClientCForm
from .filters import VenteCentreFilter
from django.contrib import messages
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Paragraph
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle
from django.http import HttpResponse
from django.db.models import F, ExpressionWrapper, DecimalField, Sum

# Create your views here.
def dashcentre(request,centre):
    return render(request,"center/dashboard/dashboardCenter.html",{"centre":centre})  

#liste des employes
def afficher_employes(request,centre):
    employes = Employe.objects.filter(centre=centre)        
    if 'q' in request.GET:
        q=request.GET['q']
        multiple_q=Q(Q(nom_e__icontains=q) | (Q(prenom_e__icontains=q)))
        employes=employes.filter(multiple_q)
    
    return render(request,"center/employes/employeList.html",{"employes":employes,"centre":centre})

#ajouter employe

def ajouter_employe(request, centre):
    centreInstance = Centre.objects.get(code_c=centre)
    if request.method == "POST":
        form = EmployeForm(request.POST)
        
        if form.is_valid():
            employe = form.save(commit=False)
            employe.centre = centreInstance
            employe.save()
            
            employe_full_name = f"{employe.nom_e} {employe.prenom_e}"
            
            messages.success(request, f'{employe_full_name} a été ajouté')
            form = EmployeForm()  
    else:
        form = EmployeForm()

    return render(request, "center/employes/employeAdd.html", {"form": form, "centre": centre})

    
#modifier employe
def modifier_employe(request,pk,centre):
    employe=Employe.objects.get(code_e=pk , centre=centre)   
    if request.method=='POST':
        form=EmployeForm(request.POST,instance=employe)
        if form.is_valid():
            form.save()
            target_url = f'/employeList/{centre}/'
            return redirect(target_url)  
    else:
        form=EmployeForm(instance=employe)
        return render(request,'center/employes/employeEdit.html',{"form":form ,"centre":centre })
    

    # Supprimer employe
def supprimer_employe(request, pk, centre):
    employe = Employe.objects.get(code_e=pk, centre=centre)

    if request.method == 'POST':
        employe.delete()
        target_url = f'/employeList/{centre}/'
        return redirect(target_url)
    else:
        form = EmployeForm(instance=employe)
    
    return render(request, 'center/employes/employeDelete.html', {"employe": employe, "centre": centre})

#imprimer employe
def imprimer_employes(request, centre):
    lignes = [["Code", "Nom", "Prénom", "Adresse", "Téléphone"]]  # Header row

    employes = Employe.objects.filter(centre=centre)

    for employe in employes:
        ligne_employe = [
            f"{employe.code_e}",
            f"{employe.nom_e}",
            f"{employe.prenom_e}",
            f"{employe.adresse_e}",
            f"{employe.telephone_e}",
        ]
        lignes.append(ligne_employe)

    pdf_filename = 'Employes.pdf'

    # Create a PDF using ReportLab
    pdf_buffer = io.BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title at the top center
    title_style = styles['Title']
    title = Paragraph("Liste des employés", title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))

    # Current date on the right
    date_style = styles['Normal']
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    date_paragraph = Paragraph(f"Date: {current_date}", date_style)
    elements.append(date_paragraph)
    elements.append(Spacer(1, 20))

    col_widths = [50, 150, 150, 150, 100]
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


#liste des clients
def afficher_clients(request,centre):
    clients = Client.objects.filter(centre=centre)        
    if 'q' in request.GET:
        q=request.GET['q']
        multiple_q=Q(Q(nom_cl__icontains=q) | (Q(prenom_cl__icontains=q)))
        clients=clients.filter(multiple_q)
    
    return render(request,"center/clients/clientList.html",{"clients":clients,"centre":centre})

#ajouter client

def ajouter_client(request, centre):
    centreInstance = Centre.objects.get(code_c=centre)
    if request.method == "POST":
        form = ClientCForm(request.POST)
        
        if form.is_valid():
            client = form.save(commit=False)
            client.centre = centreInstance
            client.save()
            
            client_full_name = f"{client.nom_cl} {client.prenom_cl}"
            
            messages.success(request, f'{client_full_name} a été ajouté')
            form = ClientCForm()  
    else:
        form = ClientCForm()

    return render(request, "center/clients/clientAdd.html", {"form": form, "centre": centre})

    
#modifier client
def modifier_client(request,pk,centre):
    client=ClientC.objects.get(code_cl=pk , centre=centre)   
    if request.method=='POST':
        form=ClientCForm(request.POST,instance=client)
        if form.is_valid():
            form.save()
            target_url = f'/clientList/{centre}/'
            return redirect(target_url)  
    else:
        form=ClientCForm(instance=client)
        return render(request,'center/clients/clientEdit.html',{"form":form ,"centre":centre })
    

    # Supprimer client
def supprimer_client(request, pk, centre):
    client = ClientC.objects.get(code_cl=pk, centre=centre)

    if request.method == 'POST':
        client.delete()
        target_url = f'/clientList/{centre}/'
        return redirect(target_url)
    else:
        form = ClientCForm(instance=client)
    
    return render(request, 'center/clients/clientDelete.html', {"client": client, "centre": centre})

def imprimer_clients(request, centre):
    lignes = [["Code", "Nom", "Prénom", "Adresse", "Téléphone", "Crédit"]]  # Header row

    clients = Client.objects.filter(centre=centre)

    for client in clients:
        ligne_client = [
            f"{client.code_cl}",
            f"{client.nom_cl}",
            f"{client.prenom_cl}",
            f"{client.adresse_cl}",
            f"{client.telephone_cl}",
            f"{client.credit}",
        ]
        lignes.append(ligne_client)

    pdf_filename = 'clients.pdf'

    # Create a PDF using ReportLab
    pdf_buffer = io.BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title at the top center
    title_style = styles['Title']
    title = Paragraph("Liste des clients", title_style)  # Updated title
    elements.append(title)
    elements.append(Spacer(1, 20))

    # Current date on the right
    date_style = styles['Normal']
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    date_paragraph = Paragraph(f"Date: {current_date}", date_style)
    elements.append(date_paragraph)
    elements.append(Spacer(1, 20))

    col_widths = [40, 100, 100, 120, 100, 60]  # Adjusted column widths
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

def afficher_produit_centre(request, centre):
    produits = produits_centre.objects.filter(centre=centre)

    if 'q' in request.GET:
        q = request.GET['q']
        # Perform case-insensitive search on designation_pc and code_pc
        multiple_q = Q(designation_pc__icontains=q) | Q(code_pc__icontains=q)
        produits = produits.filter(multiple_q)

    return render(request, "center/produits/produitCentreList.html", {"produits": produits, "centre": centre})

def imprimer_produit_centre(request, centre):
    lignes = [["Code", "Designation", "Quantite"]]  # Header row

    produits = produits_centre.objects.filter(centre=centre)

    # Create a PDF using ReportLab
    pdf_buffer = io.BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)

    # Define styles here
    styles = getSampleStyleSheet()

    elements = []

    # Current date on the right
    date_style = styles['Normal']
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    for produit in produits:
        ligne_produit = [
            f"{produit.code_pc}",
            f"{produit.designation_pc}",
            f"{produit.qte_pc}",
        ]
        lignes.append(ligne_produit)

    pdf_filename = f'produitsCentre_{centre}_{current_date}.pdf'

    # Title at the top center
    title_style = styles['Title']
    title = Paragraph(f"Liste des produits de centre {centre}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))

    # Current date on the right
    date_paragraph = Paragraph(f"Date: {current_date}", date_style)
    elements.append(date_paragraph)
    elements.append(Spacer(1, 20))

    # Adjusted column widths
    col_widths = [50, 200, 100]  # Adjust the values based on your preferences

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
def afficher_vente(request,centre):
    
    ventes = VenteCentre.objects.filter(centre=centre) 
    myFilter = VenteCentreFilter(request.GET, queryset=ventes)

    
    ventes = myFilter.qs

    ventes = ventes.annotate(
        montant_total=ExpressionWrapper(F('qte_vc') * F('prix_unitaireVTC'), output_field=DecimalField())
    )
    total_montant_total = ventes.aggregate(total=Sum('montant_total'))['total']

    context={"ventes":ventes,'myFilter':myFilter,'total_montant_total': total_montant_total, "centre":centre}
    return render(request,"center/ventes/venteList.html",context)
#ajouter vente

def ajouter_vente(request,centre):
    centreInstance = Centre.objects.get(code_c=centre)
    if request.method == "POST":          
        form=VenteCentreForm(request.POST,centre=centreInstance)
                  
        if form.is_valid():
            form.save()
            cleaned_data = form.cleaned_data
            produit_name = cleaned_data['produit'].designation_pc 
            year_of_vente = cleaned_data['date_vc'].year
            
            qte_vc = cleaned_data['qte_vc']
            prix_unitaireVTC = cleaned_data['prix_unitaireVTC']
            montant_vc = cleaned_data['montant_vc']
              
            stock_product = produits_centre.objects.get(designation_pc=produit_name,centre=centre)
            stock_product.qte_pc -= qte_vc
            stock_product.save()
            if stock_product.qte_pc<=0:
               
                success_message = f"Le produit {produit_name} est retiré du stock ."
            else :
                success_message = f"Le produit {produit_name}  est encore en stock ."
                
            
            
            

            stock_product.save()

            client_code= cleaned_data['client'].code_cl
            client= Client.objects.get(code_cl=client_code,centre=centre)
            client.credit+=(qte_vc*prix_unitaireVTC)-montant_vc
            client.save()
            vente = form.save(commit=False)
            vente.centre = centreInstance
            vente.save()
           
            
           
            messages.success(request, success_message)
            form = VenteCentreForm(centre=centreInstance)
            return render(request,"center/ventes/venteAdd.html",{"form":form, "centre": centre})
            
    else:
        form = VenteCentreForm(centre=centreInstance)
    return render(request,"center/ventes/venteAdd.html",{"form":form,"centre": centre})

##modifier vente
def modifier_vente(request,pk,centre):
    vente=VenteCentre.objects.get(num_vc=pk, centre=centre)
    
    
    initial_montant=vente.montant_vc
    if request.method=='POST':
        form=VenteCentreEditForm(request.POST,instance=vente)
        if form.is_valid():
            cleaned_data = form.cleaned_data
           
            
            
            client=vente.client
           

            montant = cleaned_data['montant_vc']   
           
            difference = montant - initial_montant
            if difference != 0:
                client.credit -= difference
                client.save()

                
            form.save()
            target_url = f'/venteCentreList/{centre}/'
            return redirect(target_url)  
    else:
        form=VenteCentreEditForm(instance=vente)
        return render(request,'center/ventes/venteEdit.html',{"form":form,"centre":centre})
##supprimer vente
def supprimer_vente(request,pk,centre):
    vente=VenteCentre.objects.get(num_vc=pk,centre=centre)   
    if request.method=='POST':     
            client = vente.client
            qte_vc = vente.qte_vc
            prix_unitaireVTC = vente.prix_unitaireVTC
            montant_vc = vente.montant_vc
            if vente.type_Paiement_vc=='Partiel':
                client.credit-=(qte_vc*prix_unitaireVTC)-montant_vc
                client.save()
            produit=vente.produit
            
            
            produit.qte_pc+=qte_vc
            produit.save()
                
            vente.delete()
               
            target_url = f'/venteCentreList/{centre}/'
            return redirect(target_url)  
    else:          
        return render(request,'center/ventes/venteDelete.html',{"vente":vente,"centre":centre})

##imprimer vente
def imprimer_vente(request,centre):
    lignes = [["Numéro", "Date","Produit","Quantité","prix unitaire","Client","Type paiement","Montant versé"]] 

    ventes = VenteCentre.objects.filter(centre=centre)
    for vente in ventes:
        ligne_vente= [
            f"{vente.num_vc}",
            f"{vente.date_vc}",
            f"{vente.produit}",
            f"{vente.qte_vc}",
            f"{vente.prix_unitaireVTC }",
            f"{vente.client}",
            f"{vente.type_Paiement_vc}",
            f"{vente.montant_vc}",
            
        ]
        lignes.append(ligne_vente)

    pdf_filename = f"Ventes_{centre}.pdf"

    # Create a PDF using ReportLab
    pdf_buffer = io.BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title at the top center
    title_style = styles['Title']
    title = Paragraph(f"Liste des ventes du centre {centre}", title_style)
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
