from django.shortcuts import render, get_object_or_404, HttpResponse
from profiles.models import Profile
from .models import Report
from sales.models import CSV,Position,Sale
from products.models import Product
from customers.models import Customer
from .utils import get_report_image
from django.http import JsonResponse
from django.views.generic import ListView,DetailView, TemplateView
from xhtml2pdf import pisa
from django.template.loader import get_template
import datetime

from django.utils.dateparse import parse_date

# Create your views here.

def create_report_view(request):
    if request.is_ajax():
        print("It is ruuning")
        report_name = request.POST.get('name')
        report_remarks = request.POST.get('remarks')
        img = request.POST.get('img')
        img_process=get_report_image(img)
        print("THe request.user is",request.user)

        author= Profile.objects.get(user=request.user)

        Report.objects.create(name=report_name,remarks=report_remarks,author=author,image=img_process)

        return JsonResponse({'msg':"pass"})
    
    return JsonResponse({})


def render_pdf_view(request, pk):
    template_path = 'reports/pdf.html'
    obj = get_object_or_404(Report, pk=pk)
    context = {'obj': obj}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="report.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
       html, dest=response)

    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def csv_upload_view(request):

    if request.method == 'POST':
        csv_file_name = request.FILES.get('file').name
        csv_file = request.FILES.get('file')
        obj,created = CSV.objects.get_or_create(file_name=csv_file)

        if created:
            obj.csv_file=csv_file
            files = csv_file.read().decode("utf-8").splitlines()
            for line in files[1:]:
                split_comma = line.split(",")
                print("The split cooma is",split_comma)
                

                split_comma[5] = datetime.datetime.strptime(split_comma[5], "%d/%m/%Y").strftime("%Y-%m-%d")
                print(split_comma[5])

                transaction_id = split_comma[1]
                product = split_comma[2]
                quantity = int(split_comma[3])
                customer = split_comma[4]
                date =parse_date(split_comma[5])   
                print("Date is",date)                  
                try:
                    product_obj = Product.objects.get(name__iexact=product)
                except Product.DoesNotExist:
                    product_obj = None
                
                

                if product_obj is not None:
                    print("The poduct values",product_obj.price)
                    print("The quantity is",quantity)

                    customer_obj, _ = Customer.objects.get_or_create(name=customer) 
                    salesman_obj = Profile.objects.get(user=request.user)
                    print("Salesman fetch")
                    position_obj = Position(product=product_obj, quantity=quantity, created=date)
                    print("BEfore save")
                    position_obj.save()
                    print("Postions created")
                    sale_obj, _ = Sale.objects.get_or_create(transaction_id=transaction_id, customer=customer_obj, salesman=salesman_obj, created=date)
                    print("Sales created")
                    sale_obj.positions.add(position_obj)
                    sale_obj.save()
            return JsonResponse({'ex': False})
        else:

            return JsonResponse({'ex': True})


                 

            

        


    
    return HttpResponse()

class UploadTemplateView(TemplateView):
    template_name = 'reports/from_file.html'

class ReportListView(ListView):
    model = Report
    template_name = 'reports/main.html'

class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/detail.html'





