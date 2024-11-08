from email.utils import parsedate
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
def Coverter_Sales(request,id):  # sourcery skip: use-named-expression
    objs1 = Estimate.objects.filter(id = id).first()
    objs2 = EstimateItem.objects.filter(estimate = objs1)
    sales = SalesOrder.objects.all().last()
    if sales:
        num = sales.sales_order_number
        sales_number = int(num.split('-')[1])
        context = {"newinvoice":objs2,'estimates':objs1,"sales_number":sales_number+1,"id":id}
    else:
        context = {"newinvoice":objs2,'estimates':objs1,"sales_number":1,"id":id}
    return render(request,"estimatesTosales.html",context)
@csrf_exempt
def Coverter_Invoice(request,id):  # sourcery skip: use-named-expression
    objs1 = Estimate.objects.filter(id = id).first()
    objs2 = EstimateItem.objects.filter(estimate = objs1)
    invoice = InvoiceEstimate.objects.all().last()
    if invoice:
        num = invoice.invoice_number
        invoice_number = int(num.split('-')[1])
        num2 = invoice.order_number
        order_number = int(num2.split('-')[1])
        context = {"newinvoice":objs2,'estimates':objs1,"invoice_number":invoice_number+1,"order_number":order_number+1,"id":id}
    else:
        context = {"newinvoice":objs2,'estimates':objs1,"invoice_number":1,"order_number":1,"id":id}
    return render(request,"createinvoiceestimates.html",context)

def Create_invoice_estimates(request,id):
    sales = Estimate.objects.get(id = id)
    params = {
        'today':datetime.date.today(),
        'sales':sales
    }
    new_invoice =  save_pdf0(params)
    return redirect(f'/media/{new_invoice}/')

################## PDF GENERATE ###############
def save_pdf0(params: dict):
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
def Newestimates(request):   # sourcery skip: avoid-builtin-shadow, use-named-expression
    requests = Request.objects.all()
    estimates = Estimate.objects.all().last()
    if estimates:
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
            id = int(name.split('-')[1])
            # print(id)
            # print(estimate_date)
            customer_name1 = Request.objects.get(id = id)
            # print(customer_name1.request)
            # print(customer_name1.price)
            # print(customer_name1)
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
            
            # print("Before saving:")
            # print("customer_name1.price =", float(data.get('total', 0.00)))
            # print("customer_name1.request =", True)

            # Update the customer's price and request status
            
            customer_name1.price = float(data.get('total', 0.00))
            customer_name1.request = True
            customer_name1.save()
            print(customer_name1.request)

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
def Coverter_Invoice_sales(request,id):  # sourcery skip: use-named-expression
    objs1 = SalesOrder.objects.filter(id = id).first()
    objs2 = SalesOrderItem.objects.filter(sales_order = objs1)
    invoice = InvoiceEstimate.objects.all().last()
    if invoice:
        num = invoice.invoice_number
        invoice_number = int(num.split('-')[1])
        num2 = invoice.order_number
        order_number = int(num2.split('-')[1])
        context = {"newinvoice":objs2,'estimates':objs1,"invoice_number":invoice_number+1,"order_number":order_number+1,"id":id}
    else:
        context = {"newinvoice":objs2,'estimates':objs1,"invoice_number":1,"order_number":1,"id":id}
    return render(request,"createinvoice.html",context)
import datetime

def Create_invoice_sales(request,id):
    sales = SalesOrder.objects.get(id = id)
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
def Newsalesorder(request):  # sourcery skip: use-named-expression
    requests = Request.objects.all()
    estimates = SalesOrder.objects.all().last()
    if estimates:
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
            estimate_id = data.get('hiddeninp')
            estimate = Estimate.objects.get(id=estimate_id) if estimate_id else None

            sales_order = SalesOrder.objects.create(
                customer_name=customer_name1.profile,
                request=customer_name1,
                estimate = estimate,
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
    context = {'objs':objs,'id':id}
    return render(request,"invoice2.html",context)


def InvoiceReal(request,id):
    sales = InvoiceEstimate.objects.get(id = id)
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
def Invoice3(request):  # sourcery skip: low-code-quality, use-named-expression
    requests = Request.objects.all()
    estimates = InvoiceEstimate.objects.all().last()
    if estimates:
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
            print("Received data:", data)  # Debugging print

            # Get dates with fallback for empty strings
            invoice_date = data.get('invoiceDate') or None
            due_date = data.get('dueDate') or None
            name = data.get('customerName', '')

            # Retrieve related customer instance
            try:
                customer_name1 = Request.objects.get(company=name)
            except Request.DoesNotExist:
                return JsonResponse({'error': 'Customer not found'}, status=404)
            # print(Estimate.objects.get(id = data.get('hiddeninp')))
            if data.get('hiddeninp2') == 'sales':
                estimate_id = data.get('hiddeninp')
                estimate_obj = SalesOrder.objects.get(id=estimate_id) if estimate_id else None
                estimate = estimate_obj.estimate
            else:
                estimate_id = data.get('hiddeninp')
                estimate = Estimate.objects.get(id=estimate_id) if estimate_id else None
            print(estimate)
            # Create the InvoiceEstimate object
            invoice = InvoiceEstimate.objects.create(
                customer_name=customer_name1.profile,
                request=customer_name1,
                estimate = estimate,
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
def Newpayment(request):  # sourcery skip: use-named-expression
    # Fetch all Request objects for the context
    requests = Request.objects.all()
    estimates = Payment.objects.all().last()
    if estimates:
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



#######################################   VENDORS PAGES   ###########################################

def Vendors1(request):
    objs = Vendor.objects.all()
    context = {'objs':objs}
    return render(request,"vendors1.html",context)

def Vendors2(request,id):
    objs = Vendor.objects.get(id = id)
    context = {'objs':objs}
    return render(request,"vendors2.html",context)

@csrf_exempt
def Vendors3(request):  # sourcery skip: extract-method
    if request.method == "POST":
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            print(data)

            # Helper function to safely convert strings to float
            def parse_float(value, default=0.0):
                try:
                    return float(value)
                except (TypeError, ValueError):
                    return default

            # Create a new Vendor instance with parsed data
            vendor = Vendor.objects.create(
                salutation=data.get('salutation', ''),
                firstname=data.get('firstname', ''),
                lastname=data.get('lastname', ''),
                companyname=data.get('companyname', ''),
                vendoremail=data.get('vendoremail', ''),
                vendorphone1=data.get('vendorphone1', ''),
                vendorphone2=data.get('vendorphone2', ''),
                gst_Treatment=data.get('gst_Treatment', ''),
                sourceofsupply=data.get('sourceofsupply', ''),
                pan=data.get('pan', ''),
                currency=data.get('currency', ''),
                openingbalance=parse_float(data.get('openingbalance', '0.00')),
                paymentterms=data.get('paymentterms', ''),
                pricelist=data.get('pricelist', ''),
                enableportal=data.get('enableportal', '') == 'on',
                portallanguage=data.get('portallanguage', ''),
                documents=data.get('documents', ''),
                billingattention=data.get('billingattention', ''),
                billingcountry=data.get('billingcountry', ''),
                billingaddress1=data.get('billingaddress1', ''),
                billingaddress2=data.get('billingaddress2', ''),
                billingcity=data.get('billingcity', ''),
                billingstate=data.get('billingstate', ''),
                billingpincode=data.get('billingpincode', ''),
                billingphone=data.get('billingphone', ''),
                shippingattention=data.get('shippingattention', ''),
                shippingcountry=data.get('shippingcountry', ''),
                shippingaddress1=data.get('shippingaddress1', ''),
                shippingaddress2=data.get('shippingaddress2', ''),
                shippingcity=data.get('shippingcity', ''),
                shippingstate=data.get('shippingstate', ''),
                shippingpincode=data.get('shippingpincode', ''),
                shippingphone=data.get('shippingphone', '')
            )
            vendor.full_clean()  # Validates the Vendor instance

            # If successful, return success message
            messages.success(request, "Vendor created successfully.")
            return JsonResponse({'message': 'Vendor created successfully'}, status=201)

        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return render(request, "vendors3.html")


def Purchases1(request):
    objs = Purchase.objects.all()
    context = {'objs':objs}
    return render(request,"purchases1.html",context)

def Purchases2(request,id):
    objs = Purchase.objects.get(id = id)
    context = {'objs':objs,'id':id}
    return render(request,"purchases2.html",context)

@csrf_exempt
def PurchasesToBill(request,id):  # sourcery skip: use-named-expression
    objs1 = Purchase.objects.get(id = id)
    objs2 = PurchaseItem.objects.filter(invoice = objs1)
    last_bill = Bill.objects.all().last()
    if last_bill:
        print(last_bill.bill_number)
        bill1 = last_bill.bill_number
        bill_number = int(bill1.split('-')[1])
        # print(bill_number)
        context = {"objs1": objs1,"objs2":objs2, "bill_number": bill_number+1,'id':id}
    else:
        context = {"objs1": objs1,"objs2":objs2, "bill_number": 1,'id':id}
    return render(request,"PurchasesToBill.html",context)


@csrf_exempt
def Purchases3(request):  # sourcery skip: use-named-expression
    vendors = Vendor.objects.all()
    purchase = Purchase.objects.all().last()
    if purchase:
        num = purchase.purchase_order
        # print(num)
        sales_number = int(num.split('-')[1])
        # print(estimate_number)
        context = {"objs":vendors,"purchase_number":sales_number+1}
    else:
        context = {"objs":vendors,"purchase_number":1}
    
    if request.method == "POST":
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            name = data.get('vendorName', 'Select or add Vendor')
            vendorid = int(name.split('-')[1])
            vendor = Vendor.objects.get(id = vendorid)

            
            # Create Purchase instance
            invoice = Purchase.objects.create(
                vendor_name=vendor,
                source_of_supply=data.get('SourceOfSupply', ''),
                destination_of_supply=data.get('DestinationOfSupply', ''),
                purchase_order=data.get('purchaseorder', ''),
                reference=data.get('reference', ''),
                date=data.get('date', ''),
                expected_delivery_date=data.get('expected_delivery_date', ''),
                payment_terms=data.get('paymentterms', ''),
                item_tax=data.get('itemtax', 'none'),
                price_list=data.get('pricelist', 'none'),
                discount=data.get('discount', 'none'),
                sub_total=float(data.get('subTotal', '0.00')),
                shipping_charges=float(data.get('shippingCharges', '0.00')),
                adjustment=float(data.get('adjustment', '0.00')),
                total=float(data.get('total', '0.00')),
            )
            
            # Create associated PurchaseItems
            for item_data in data.get('items', []):
                PurchaseItem.objects.create(
                    invoice=invoice,
                    item_details=item_data.get('itemDetails', ''),
                    quantity=int(item_data.get('quantity', 0)),
                    rate=float(item_data.get('rate', '0.00')),
                    discount=float(item_data.get('discount', '0.00')),
                    tax=item_data.get('tax', ''),
                    amount=float(item_data.get('amount', '0.00')),
                )
            
            return JsonResponse({'message': 'Invoice created successfully'}, status=201)
        
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return render(request, "purchases3.html", context)


def Bills1(request):
    objs = Bill.objects.all()
    context = {'objs':objs}
    return render(request,"bills1.html",context)

def Bills2(request,id):
    objs = Bill.objects.get(id = id)
    # print(objs.vendor_name)
    context = {'objs':objs}
    return render(request,"bills2.html",context)

@csrf_exempt
def Bills3(request):  # sourcery skip: use-named-expression
    vendors = Vendor.objects.all()
    last_bill = Bill.objects.all().last()
    if last_bill:
        print(last_bill.bill_number)
        bill1 = last_bill.bill_number
        bill_number = int(bill1.split('-')[1])
        # print(bill_number)
        context = {"objs": vendors, "bill_number": bill_number+1}
    else:
        context = {"objs": vendors, "bill_number": 1}

    if request.method == "POST":
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            # print(data)
            name = data.get('vendorName', 'Select or add Vendor')
            # print(name)
            vendorid = int(name.split('-')[1])
            # print(vendorid)
            vendor = Vendor.objects.get(id = vendorid)
            # print(vendor)

            # Create Bill instance
            bill = Bill.objects.create(
                vendor_name=vendor,
                source_of_supply=data.get('SourceOfSupply', ''),
                destination_of_supply=data.get('DestinationOfSupply', ''),
                bill_number=data.get('bill', ''),
                reference=data.get('ordernumber', ''),
                bill_date=data.get('billdate', ''),
                due_date=data.get('duedate', ''),
                payment_terms=data.get('paymentterms', ''),
                item_tax=data.get('itemtax', 'none'),
                price_list=data.get('pricelist', 'none'),
                discount=data.get('discount', 'none'),
                sub_total=float(data.get('subTotal', '0.00')),
                shipping_charges=float(data.get('shippingCharges', '0.00')),
                adjustment=float(data.get('adjustment', '0.00')),
                total=float(data.get('total', '0.00')),
            )
            # print(data.get('hiddeninp'))
            hiddeninp = data.get('hiddeninp')
            if hiddeninp:
                billu = Purchase.objects.get(id = data.get('hiddeninp'))
                billu.status = 'BILLED'
                billu.save()


            # Create associated BillItems
            for item_data in data.get('items', []):
                BillItem.objects.create(
                    bill=bill,
                    item_details=item_data.get('itemDetails', ''),
                    quantity=int(item_data.get('quantity', 0)),
                    rate=float(item_data.get('rate', '0.00')),
                    discount=float(item_data.get('discount', '0.00')),
                    tax=item_data.get('tax', ''),
                    amount=float(item_data.get('amount', '0.00')),
                )

            return JsonResponse({'message': 'Bill created successfully'}, status=201)

        except Vendor.DoesNotExist:
            return JsonResponse({'error': 'Vendor not found'}, status=404)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, "bills3.html", context)


def Payments1(request):
    return render(request,"paymentvendor1.html")
def Payments2(request):
    return render(request,"paymentvendor2.html")
def Payments3(request):
    return render(request,"paymentvendor3.html")



def Expansens1(request):
    return render(request,"espanses1.html")


def Expansens2(request):
    return render(request,"espanses2.html")

@csrf_exempt
def Expansens3(request):  # sourcery skip: use-named-expression
    # Handling GET request to display the form with vendors and an invoice number
    if request.method == "POST":
        vendors = Vendor.objects.all()
        last_expense = Expense.objects.all().last()
        
        # Generate the next invoice number if there is an existing expense
        if last_expense:
            last_invoice_number = int(last_expense.invoice_number.split('-')[1])
            next_invoice_number = f"EXP-{last_invoice_number + 1}"
        else:
            next_invoice_number = "EXP-1"
        
        # context = {
        #     "vendors": vendors,
        #     "next_invoice_number": next_invoice_number
        # }
    
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)

            # Get or validate vendor by parsing the vendor ID from the provided data
            vendor_name = data.get('vendor', 'Select or add Vendor')
            vendor_id = int(vendor_name.split('-')[1]) if '-' in vendor_name else None
            vendor = Vendor.objects.get(id=vendor_id) if vendor_id else None

            # Create Expense instance
            expense = Expense.objects.create(
                start_date=data.get('startDate', None),
                expense_account=data.get('expenseAccount', ''),
                amount=float(data.get('amount', '0.00')),
                paid_through=data.get('paidThrough', ''),
                expense_type=data.get('expenseType', ''),
                sac=data.get('sac', ''),
                vendor=vendor,
                gst_treatment=data.get('gstTreatment', ''),
                source_of_supply=data.get('sourceOfSupply', ''),
                destination_of_supply=data.get('destinationOfSupply', ''),
                reverse_charge=data.get('reverseCharge', False),
                tax=float(data.get('tax', '0.00')),
                invoice_number=data.get('invoiceNumber', ''),
                notes=data.get('notes', ''),
                customer_name=data.get('customerName', 'Select or add customer')
            )

            return JsonResponse({'message': 'Expense created successfully'}, status=201)

        except Vendor.DoesNotExist:
            return JsonResponse({'error': 'Vendor not found'}, status=404)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)},status=500)
    return render(request,"espanses3.html")


def ReccuringExpanses1(request):
    return render(request,"reccuring1.html")

def ReccuringExpanses2(request):
    return render(request,"reccuring2.html")

@csrf_exempt
def ReccuringExpanses3(request):
    # Handling GET request to display the form with vendors
    if request.method == "POST":
        vendors = Vendor.objects.all()
        context = {"vendors": vendors}
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)

            # Get or validate vendor by parsing the vendor ID from the provided data
            vendor_name = data.get('vendor', 'Select or add Vendor')
            vendor_id = int(vendor_name.split('-')[1]) if '-' in vendor_name else None
            vendor = Vendor.objects.get(id=vendor_id) if vendor_id else None

            # Create Expense instance
            expense = Expense.objects.create(
                start_date=data.get('startDate', None),
                expense_account=data.get('expenseAccount', ''),
                amount=float(data.get('amount', '0.00')),
                paid_through=data.get('paidThrough', ''),
                expense_amount=float(data.get('expenseamount', '0.00')),
                expense_type=data.get('expenseType', ''),
                sac=data.get('sac', ''),
                vendor=vendor,
                gst_treatment=data.get('gstTreatment', ''),
                source_of_supply=data.get('sourceOfSupply', ''),
                destination_of_supply=data.get('destinationOfSupply', ''),
                reverse_charge=data.get('reverseCharge', False),
                tax=float(data.get('tax', '0.00')),
                notes=data.get('notes', ''),
                customer_name=data.get('customerName', 'Select or add customer')
            )

            return JsonResponse({'message': 'Expense created successfully'}, status=201)

        except Vendor.DoesNotExist:
            return JsonResponse({'error': 'Vendor not found'}, status=404)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return render(request, "reccuring2.html", context)
