from django.shortcuts import render,HttpResponse,redirect
from krupa.models import *
from admin_panel.models import Managers
from django.core import serializers
from django.core.serializers import serialize
from rest_framework.renderers import JSONRenderer
from .serializer import *
from django.contrib import messages
from .models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from krupa.models import Estimate, EstimateItem
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
import uuid
from django.conf import settings
import os


# Create your views here.

def AdminProducts(request):
    products = Products.objects.all()
    context = {'products':products}
    return render(request,"admin_products.html",context)

def AddProducts(request):
    category = Category.objects.all()
    sub_category = Subcategory.objects.all()
    serializer = SubcategorySerializer(sub_category,many =True)
    # print(serializer)
    sub = JSONRenderer().render(serializer.data).decode('utf-8')
    # print(sub)
    context = {'category':category,'sub_category':sub_category,'sub':sub}

    if request.method == "POST":
        # Extracting form data
        product_name = request.POST.get('product-name')
        category = request.POST.get('category')
        subcategory = request.POST.get('sub-category')
        brand = request.POST.get('brand')
        description = request.POST.get('description')
        size = request.POST.get('add-size')
        date = request.POST.get('product-date')
        
        # Handle file upload (for images)
        product_images = request.FILES.get('product-images')

        cat = Category.objects.filter(category_name = category).first()
        sub_cat = Subcategory.objects.filter(sub_name = subcategory).first()

        if not cat:
            return HttpResponse("Invalid Category")
        if not sub_cat:
            return HttpResponse("Invalid Sub Category")

        # Assuming you have a Product model, save the new product
        new_product = Products.objects.create(
            product_name=product_name,
            category=cat,
            subcategory=sub_cat,
            brand=brand,
            descripton=description,
            size=size,
            date=date,
            product_image = product_images,
        )
        new_product.save()
        # product_images = request.FILES.getlist('product-images')
        # print(request.POST)
        # print(product_images)
    return render(request,"add_products.html",context)

def AddSubCategories(request):
    category = Category.objects.all()
    context = {'category':category}
    if request.method == "POST":
        category = request.POST.get('category')
        sub_name = request.POST.get('sub-category')
        sub_image = request.FILES.get('product-images')
        description = request.POST.get('description')
        size = request.POST.get('size')
        date = request.POST.get('product-date')

        cat = Category.objects.filter(category_name = category).first()

        if not cat:
            return HttpResponse("Invalid Category")

        new_sub_category = Subcategory.objects.create(
            category = cat,
            sub_name = sub_name,
            sub_image = sub_image,
            description = description,
            size = size,
            date = date
        )

        new_sub_category.save()
    return render(request,"addsubcategories.html",context)

def AddCategories(request):
    if request.method == "POST":
        # category = request.POST.get('category')
        category = request.POST.get('category')
        sub_image = request.FILES.get('product-images')
        description = request.POST.get('description')
        size = request.POST.get('size')
        date = request.POST.get('product-date')

        # cat = Category.objects.filter(category_name = category).first()

        # if not cat:
        #     return HttpResponse("Invalid Category")

        new_category = Category.objects.create(
            category_name = category,
            category_image = sub_image,
            description = description,
            size = size,
            date = date
        )

        new_category.save()
    return render(request,"addcategories.html")


def Leads1(request):
    leads = Request.objects.all()
    context = {'leads':leads}
    return render(request,"leads-1.html",context)

def Leads2(request):
    leads = Request.objects.all()
    context = {'leads':leads}
    return render(request,"leads-2.html",context)

def Leads3(request):
    leads = Request.objects.all()
    context = {'leads':leads}
    return render(request,"leads-3.html",context)

def Customers(request):  # sourcery skip: avoid-builtin-shadow, extract-method
    obj = Request.objects.all()
    manager = Managers.objects.all()
    context = {'obj':obj,'manager':manager}
    if request.method == 'POST':
        # print(request.POST)
        data = request.POST
        id = data.get('id')
        name = data.get('manager').strip()
        request_id = Request.objects.get(id = id)
        print(request_id)
        manager_name = Managers.objects.filter(displayname__iexact = name).first()
        request_id.manager = manager_name
        request_id.save()
    return render(request,"sales-customers-1.html",context)

############################ MANAGERS PAGES #############################

def ManagersView(request):
    managers = Managers.objects.all()
    context = {'managers':managers}
    return render(request,"Managers.html",context)

def AddManagers(request):
    if request.method == "POST":
        data = request.POST
        print(data)
        manager = Managers.objects.create(
            firstname = data.get('firstname'),
            lastname = data.get('lastname'),
            displayname= data.get('name'),
            email = data.get('email'),
            work_phone = data.get('phone1'),
            emergency_phone = data.get('phone2'),
        )
        manager.save()
    
    return render(request,"AddManager.html")


########################### NEW ESTIMATES #############################

def Estimates(request):
    objs = Estimate.objects.all()
    context = {'estimates':objs}
    return render(request,"Estimates.html",context)

def Estimates2(request,id):
    objs = Estimate.objects.get(id = id)
    context = {'data':objs,'id':id}
    return render(request,"Estimates2.html",context)
@csrf_exempt
def Coverter_Invoice(request,id):
    objs1 = Estimate.objects.filter(id = id).first()
    objs2 = EstimateItem.objects.filter(estimate = objs1)
    invoice = InvoiceEstimate.objects.all().last()
    print(invoice)
    if invoice:
        num = invoice.invoice_number
        invoice_number = int(num.split('-')[1])
        num2 = invoice.order_number
        order_number = int(num2.split('-')[1])
        context = {"newinvoice":objs2,'estimates':objs1,"invoice_number":invoice_number+1,"order_number":order_number+1,"id":id}
    else:
        context = {"newinvoice":objs2,'estimates':objs1,"invoice_number":1,"order_number":1,"id":id}
    return render(request,"createinvoiceestimates.html",context)


@csrf_exempt
def Newestimates(request):  # sourcery skip: low-code-quality
    requests = Request.objects.all()
    if estimates := Estimate.objects.all().last():
        num = estimates.estimate_number
        estimate_number = int(num.split('-')[1])
        # print(estimate_number)
        context = {"custoumers":requests,"estimate_number":estimate_number+1}
    else:
        context = {"custoumers":requests,"estimate_number":1}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # print(data)
            estimate_date = data.get('estimateDate', None) if data.get('estimateDate') else None
            expiry_date = data.get('expiryDate', None) if data.get('expiryDate') else None
            name = data.get('customerName', '')
            # print(estimate_date)
            customer_name1 = Request.objects.get(company = name)
            # print(customer_name1)
            # for item in data.get('items', []):
            #     amount = item.get('itemDetails', 0.00)  # Get the amount for the current item, default to 0.00 if not found
            #     print(amount)  # Print the amount

            # Create the Estimate object
            # print(data.createRetainerInvoice)
            estimate = Estimate.objects.create(
                customer_name=customer_name1.profile,
                request = customer_name1,
                billing_address=data.get('billingAddress', ''),
                shipping_address=data.get('shippingAddress', ''),
                place_of_supply=data.get('placeOfSupply', 'Select place of supply'),
                estimate_number=data.get('estimateNumber', ''),
                reference=data.get('reference', ''),
                estimate_date=estimate_date,
                expiry_date=expiry_date,
                sales_person=data.get('salesPerson', ''),
                project_name=data.get('projectName', ''),
                subject=data.get('subject', ''),
                sub_total = float(data.get('subTotal', 0.00)),
                shipping_charges = float(data.get('shippingCharges', 0.00)),
                adjustment = float(data.get('adjustment', 0.00)),
                total=data.get('total', '0.00'),
                terms_and_conditions=data.get('termsAndConditions', ''),
                create_retainer_invoice=data.get('createRetainerInvoice', False)
            )
            
            

            # Create the related EstimateItem objects
            for item in data['items']:
                EstimateItem.objects.create(
                    estimate=estimate,
                    item_details=item.get('itemDetails', ''),
                    quantity = float(item.get('quantity', 0.00)) if item.get('quantity') else 0.00,
                    rate = float(item.get('rate', 0.00)) if item.get('rate') else 0.00,
                    discount=item.get('discount', '0 %'),
                    tax=item.get('tax', 'Select a Tax'),
                    amount = float(item.get('amount', 0.00)) if item.get('amount') else 0.00
                )

            messages.success(request,"New estimate created successfully")
            # return redirect("newestimates/")

            return JsonResponse({'message': 'Estimate created successfully'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, "newestimates.html",context)



########################### Sales Orders #############################

def SalesOrder1(request):
    objs = SalesOrder.objects.all()
    context = {'salesorders': objs}
    return render(request,"salesorder1.html",context)

def SalesOrder2(request,id):
    data = SalesOrder.objects.get(id =id)
    context = {"data":data,"id":id}
    return render(request,"salesorder2.html",context)


@csrf_exempt
def Coverter_Invoice_sales(request,id):
    objs1 = SalesOrder.objects.filter(id = id).first()
    objs2 = SalesOrderItem.objects.filter(sales_order = objs1)
    if invoice := InvoiceEstimate.objects.all().last():
        num = invoice.invoice_number
        invoice_number = int(num.split('-')[1])
        num2 = invoice.order_number
        order_number = int(num2.split('-')[1])
        context = {"newinvoice":objs2,'estimates':objs1,"invoice_number":invoice_number+1,"order_number":order_number+1,"id":id}
    else:
        context = {"newinvoice":objs2,'estimates':objs1,"invoice_number":1,"order_number":1,"id":id}
    return render(request,"createinvoice.html",context)
import datetime

def Create_invoice_sales(request):
    sales = SalesOrder.objects.all()
    params = {
        'today':datetime.date.today(),
        'sales':sales
    }
    new_invoice =  save_pdf(params)
    return redirect(f'/media/{new_invoice}/')

################## PDF GENERATE ###############
def save_pdf(params: dict):
    template = get_template("invoice.html")
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
    file_name = f"{uuid.uuid4()}.pdf"
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    try:
        # Save PDF file to the specified path
        with open(file_path, 'wb+') as output:
            pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
    except Exception as e:
        print(f"Error saving PDF: {e}")
        return None

    return file_name


@csrf_exempt
def Newsalesorder(request):
    requests = Request.objects.all()
    if estimates := SalesOrder.objects.all().last():
        num = estimates.sales_order_number
        sales_number = int(num.split('-')[1])
        # print(estimate_number)
        context = {"custoumers":requests,"sales_number":sales_number+1}
    else:
        context = {"custoumers":requests,"sales_number":1}

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # print(data.get('salesOrderDate'))
            name = data.get('customerName', '')
            customer_name1 = Request.objects.get(company=name)

            sales_order = SalesOrder.objects.create(
                customer_name=customer_name1.profile,
                request=customer_name1,
                sales_order_number=data.get('salesOrderNumber', ''),
                reference_number=data.get('referenceNumber', ''),
                sales_order_date=data.get('salesOrderDate', None),
                expected_shipment_date=data.get('expectedShipmentDate', None),
                payment_terms=data.get('paymentTerms', ''),
                delivery_method=data.get('deliveryMethod', ''),
                sales_person=data.get('salesPerson', ''),
                sub_total=float(data.get('subTotal', '0.00')),
                shipping_charges=float(data.get('shippingCharges', '0.00')),
                adjustment=float(data.get('adjustment', '0.00')),
                total=float(data.get('total', '0.00')),
                terms_and_conditions=data.get('termsAndConditions', ''),
                create_retainer_invoice=data.get('createRetainerInvoice', False)
            )
            # print(data.get('items'))
            # sales_order.full_clean()
            for item_data in data.get('items', []):
                # print(item_data)
                sales_order_item = SalesOrderItem.objects.create(
                    sales_order=sales_order,
                    item_details=item_data.get('itemDetails', ''),
                    quantity=float(item_data.get('quantity', 0.00)),
                    rate=float(item_data.get('rate', 0.00)),
                    discount=item_data.get('discount', '0 %'),
                    tax=item_data.get('tax', 'Select a Tax'),
                    amount=float(item_data.get('amount', 0.00))
                )
                sales_order_item.full_clean()

            messages.success(request, "Sales order created successfully.")
            return JsonResponse({'message': 'Sales order created successfully'}, status=201)

        except Request.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)
        except ValidationError as e:
            return JsonResponse({'error': f'Validation Error: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, "salesorder.html", context)


########################### Invoices #############################
def Invoice1(request):
    objs = InvoiceEstimate.objects.all()
    context = {'invoice':objs}
    return render(request,"invoice1.html",context)

def Invoice2(request,id):
    objs = InvoiceEstimate.objects.get(id = id)
    context = {'objs':objs}
    return render(request,"invoice2.html",context)


def InvoiceReal(request):
    sales = InvoiceEstimate.objects.all()
    params = {
        'today':datetime.date.today(),
        'invoice':sales
    }
    new_invoice =  save_pdf2(params)
    return redirect(f'/media/{new_invoice}/')

def save_pdf2(params: dict):
    template = get_template("invoice.html")
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
    file_name = f"{uuid.uuid4()}.pdf"
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    try:
        # Save PDF file to the specified path
        with open(file_path, 'wb+') as output:
            pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
    except Exception as e:
        print(f"Error saving PDF: {e}")
        return None

    return file_name

# from .models import Customer, Invoice, Item
from django.core.exceptions import ValidationError
@csrf_exempt
def Invoice3(request):  # sourcery skip: low-code-quality
    requests = Request.objects.all()
    if estimates := InvoiceEstimate.objects.all().last():
        num = estimates.invoice_number
        num2 = estimates.order_number
        # print(num)
        sales_number = int(num.split('-')[1])
        order = int(num2.split('-')[1])
        # print(estimate_number)
        context = {"custoumers":requests,"invoice_number":sales_number+1,"order":order+1}
    else:
        context = {"custoumers":requests,"invoice_number":1,"order":1}
    if request.method == "POST":
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            # print("Received data:", data)  # Debugging print

            # Get dates with fallback for empty strings
            invoice_date = data.get('invoiceDate') or None
            due_date = data.get('dueDate') or None
            name = data.get('customerName', '')

            # Retrieve related customer instance
            try:
                customer_name1 = Request.objects.get(company=name)
            except Request.DoesNotExist:
                return JsonResponse({'error': 'Customer not found'}, status=404)
            print(data.get('invoiceDate'))

            # Create the InvoiceEstimate object
            invoice = InvoiceEstimate.objects.create(
                customer_name=customer_name1.profile,
                request=customer_name1,
                invoice_number=data.get('invoiceNumber', ''),
                order_number=data.get('orderNumber', ''),
                invoice_date=invoice_date,
                terms=data.get('terms', ''),
                due_date=due_date,
                sales_person=data.get('salesPerson', ''),
                sub_total=float(data.get('subTotal', '0.00') or 0.00),
                shipping_charges=float(data.get('shippingCharges', '0.00') or 0.00),
                adjustment=float(data.get('adjustment', '0.00') or 0.00),
                total=float(data.get('total', '0.00')),
                terms_and_conditions=data.get('termsAndConditions', ''),
                create_retainer_invoice=data.get('createRetainerInvoice', False)
            )
            if(data.get('createRetainerInvoice') == True):
                # print("entered")
                if(data.get('hiddeninp1') == "estimates"):
                    # print("hello")
                    estimate = Estimate.objects.get(id = data.get('hiddeninp'))
                    estimate.status = "Invoiced"
                    estimate.save()
                elif(data.get('hiddeninp2') == "sales"):
                    # print("hi")
                    estimate = SalesOrder.objects.get(id = data.get('hiddeninp'))
                    estimate.satus = "Invoiced"
                    estimate.save()

            # Create related Item objects for the invoice
            for item_data in data.get('items', []):
                item = Item.objects.create(
                    invoice=invoice,
                    item_details=item_data.get('itemDetails', ''),
                    quantity=float(item_data.get('quantity', 0.00)),
                    rate=float(item_data.get('rate', 0.00)),
                    discount=item_data.get('discount', '0 %'),
                    tax=item_data.get('tax', 'Select a Tax'),
                    amount=float(item_data.get('amount', 0.00))
                )

            # On successful creation, send a success message
            messages.success(request, "Invoice created successfully.")
            return JsonResponse({'message': 'Invoice created successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': f"Validation error: {e.message_dict}"}, status=400)
        except TypeError as e:
            return JsonResponse({'error': f"Type conversion error: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({'error': f"Unexpected error: {str(e)}"}, status=400)

    # If it's a GET request, return the form
    return render(request, "invoice3.html", context)


########################### Payment ################################

def Payment1(request):
    objs = Payment.objects.all()
    context = {'payments':objs}
    return render(request,"payment1.html",context)


def Payment2(request,id):
    objs = Payment.objects.get(id = id)
    context = {'objs':objs}
    return render(request,"payments2.html",context)



def PaymentInvoice(request):
    pay = Payment.objects.all()
    params = {
        'today':datetime.date.today(),
        'invoice':pay
    }
    new_invoice =  save_pdf3(params)
    return redirect(f'/media/{new_invoice}/')

def save_pdf3(params: dict):
    template = get_template("invoice.html")
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
    file_name = f"{uuid.uuid4()}.pdf"
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    try:
        # Save PDF file to the specified path
        with open(file_path, 'wb+') as output:
            pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
    except Exception as e:
        print(f"Error saving PDF: {e}")
        return None

    return file_name

@csrf_exempt
def Newpayment(request):
    # Fetch all Request objects for the context
    requests = Request.objects.all()
    if estimates := Payment.objects.all().last():
        num = estimates.payment_number
        # print(num)
        sales_number = int(num.split('-')[1])
        # print(estimate_number)
        context = {"custoumers":requests,"payment_number":sales_number+1}
    else:
        context = {"custoumers":requests,"payment_number":1}

    if request.method == "POST":
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            print(data)
            
            # Retrieve related Request object based on customer name
            customer_name = data.get('customerName', '')
            request_instance = Request.objects.get(company=customer_name)

            # Parse dates and numeric fields with fallback defaults
            payment_date = data.get('paymentDate', None)
            amount_received = float(data.get('amountReceived', '0.00'))
            bank_charge = float(data.get('bankCharge', '0.00'))
            sub_total = float(data.get('subTotal', '0.00'))
            shipping_charges = float(data.get('shippingCharges', '0.00'))
            adjustment = float(data.get('adjustment', '0.00'))
            total = float(data.get('total', '0.00'))

            # Create the Payment object
            payment = Payment.objects.create(
                customer_name=request_instance.profile,
                request=request_instance,
                amount_received=amount_received,
                bank_charge=bank_charge,
                payment_date=payment_date,
                payment_number=data.get('paymentNumber', ''),
                payment_mode=data.get('paymentMode', ''),
                deposited_to=data.get('depositedTo', ''),
                reference=data.get('reference', ''),
                tax_deducted=data.get('taxDeducted', 'yes'),
                reference_number=data.get('referenceNumber', ''),
                sub_total=sub_total,
                shipping_charges=shipping_charges,
                adjustment=adjustment,
                total=total
            )
            payment.full_clean()  # Validates the Payment instance

            # If successful, return success message
            messages.success(request, "Payment created successfully.")
            return JsonResponse({'message': 'Payment created successfully'}, status=201)

        except Request.DoesNotExist:
            return JsonResponse({'error': 'Request instance not found'}, status=404)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    # For a GET request, render the HTML template with context
    return render(request,"newpayment.html",context)




# ############### GENERATING PDF ############


# def save_pdf(params: dict):
#     template = get_template("invoice.html")
#     html = template.render(params)
#     response = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
#     file_name = f"{uuid.uuid4()}.pdf"
#     file_path = os.path.join(settings.MEDIA_ROOT, file_name)

#     try:
#         # Save PDF file to the specified path
#         with open(file_path, 'wb+') as output:
#             pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
#     except Exception as e:
#         print(f"Error saving PDF: {e}")
#         return None

#     return file_name
