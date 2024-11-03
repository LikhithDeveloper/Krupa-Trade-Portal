from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
import json
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import JSONRenderer
from .serializer import *
from .serializer import SupportTicketSerializer
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.serializers import serialize

# Create your views here.

def login_view(request):  # sourcery skip: avoid-builtin-shadow
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Debugging: Check if user exists
        try:
            user = CustomUser.objects.get(email=email)
            print(f"User found: {user.email}")
        except CustomUser.DoesNotExist:
            print("No user with this email")

        # Authenticate
        profile = authenticate(email=email, password=password)
        print(f"Profile: {profile}")  # Debugging: Check if authentication works

        if profile is not None:
            login(request, profile)
            id = user.id
            return redirect('/')
        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return render(request, "login.html")
    return render(request, "login.html")

def register_view(request):  # sourcery skip: avoid-builtin-shadow
    if request.method == "POST":
        try:
            return _extracted_from_register_view_4(request)
        except IntegrityError:
            return JsonResponse({'success':False,"error":"Email already exits"},status = 400)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({'success':False,"error": str(e)},status = 500)

    return render(request, 'register.html')


# TODO Rename this here and in `register_view`
def _extracted_from_register_view_4(request):
    data = json.loads(request.body)
    print(data)
    if CustomUser.objects.filter(email = data['email']).exists():
        return JsonResponse({'success':False,"error":"Email already exits"},status = 400)
    user = CustomUser.objects.create(
        email = data['email'],
        # password = data['password'],
        gstin = data['gstin'],
        username = data['email'],
        phone_number = data['phone']
    )
    user.set_password(data['password'])
    user.save()
    context = {'id', user.id}
    return JsonResponse({'success': True, 'redirect_url': '/login/'})


def order_details_view(request,id):
    user_details = Orders.objects.filter(id = id).first()
    profile = CustomUser.objects.filter(email = user_details.profile).first()
    address_user = UserAddress.objects.filter(profile = profile).first()
    # print(profile.email)
    context = { 'user':profile,'address':address_user,'id':profile.id }
    return render(request, "oder_details.html",context)


@login_required
def order_view(request, id):
    context = {'id':id}  # Initialize context with a default value
    try:
        user = CustomUser.objects.get(id=id)
        print(user)
        orders = Orders.objects.filter(profile=user)
        # print(orders)
        # order_id = orders[0].id
        # orders_json = serialize('json', orders)  # Serialize the queryset to JSON
        # print(orders_json)
        serializer = OrdersSerializer(orders, many=True)
        orders_json = JSONRenderer().render(serializer.data)
        print(orders_json)
        
        if not orders.exists():  # Check if there are no orders
            context = {'orders': orders_json.decode('utf-8'), 'id': id}
            # print(context)
        else:
            order_id = orders[0].id
            context = {'orders': orders_json.decode('utf-8'), 'id': id, 'order_id': order_id}

        
    except Orders.DoesNotExist:
        context = {'error': 'Order not found'}
        print("Hi 1")
        
    except Exception as e:
        context = {'error': str(e)}


    return render(request, 'order.html', context)


@login_required
def products_view(requset):  # sourcery skip: avoid-builtin-shadow
    category = Category.objects.all()
    subcategory = Subcategory.objects.all()
    products = Products.objects.all()
    subcategory_json = SubcategorySerializer(subcategory,many = True)
    subcategory_json1 = JSONRenderer().render(subcategory_json.data)
    serializer = ProductSerializer(products, many=True)
    products_json = JSONRenderer().render(serializer.data)
    context = {'id':requset.user.id ,'category':category,'subcategory':subcategory, 'product':products_json.decode('utf-8'),'subcategory1':subcategory_json1.decode('utf-8')}
    if requset.method == "POST":
        data = requset.POST
        print(data)
        product_name = data.get("product")
        quantity = data.get("quantity")
        company = data.get("company")
        pincode = data.get("pincode")
        email = data.get("email")
        mobile_number = data.get("mobile")
        profile = CustomUser.objects.filter(id=requset.user.id).first()
        type = data.get('type')
        request_model = Request.objects.create(
            profile = profile,
            product_name = product_name,
            quantity = quantity,
            company = company,
            pincode = pincode,
            email = email,
            mobile_number = mobile_number,
            type = type
        )
        request_model.save()
    return render(requset,"products.html",context)


def request_view(request,id):
    profile = CustomUser.objects.filter(id=id).first()
    requests = Request.objects.filter(profile=profile)
    # print(requests)
    context = {'id':id ,'requests':requests}
    return render(request,"request.html",context)

from django.core import serializers
@login_required
def support_ticket_view_1(request,id):
    profile = CustomUser.objects.get(id = id)
    tickets = SupportTicket.objects.filter(profile = profile)
    # serializer = SupportTicketSerializer(tickets,many = True)
    # ticket_json = JSONRenderer().render(serializer.data).decode('utf-8')
    # print(ticket_json)
    ticket_json = serializers.serialize('json',tickets)
    print(ticket_json)
    context = {
        'id': id,
        'tickets': ticket_json  # Decode JSON bytes to string
    }
    # print(context)
    return render(request,"supportticket.html",context)


@login_required
def support_ticket_view_2(request,id):
    profile = CustomUser.objects.get(id = id)
    context = {'id':id}
    if request.method == "POST":
        data = request.POST
        ticket = SupportTicket.objects.create(
            profile = profile,
            department = data.get("department"),
            subject = data.get("subject"),
            message = data.get("message"),
            additional_email = data.get("email-recipients")
        )
        ticket.save()
        return redirect(f'/support/{id}/')
    return render(request,"supportticket1.html",context)


@login_required
def account_view(request, id):
    data = CustomUser.objects.get(id=id)
    req = Request.objects.filter(profile=data)
    info = CompanyInfo.objects.filter(user=data).first()

    if request.method == "POST":
        data1 = request.POST
        
        # Handle Company Info Form Submission
        if 'company_name' in data1:
            if CompanyInfo.objects.filter(user=data).exists():
                cmpy_info = CompanyInfo.objects.filter(user=data).first()
                cmpy_info.company_name = data1.get('company_name')
                cmpy_info.pan = data1.get('pan_number')
                cmpy_info.gstno = data1.get('gst_number')
                cmpy_info.cinno = data1.get('cin_number')
                messages.success(request, "Company info updated successfully.")
            else:
                cmpy_info = CompanyInfo.objects.create(
                    user=data,
                    company_name=data1.get('company_name'),
                    pan=data1.get('pan_number'),
                    gstno=data1.get('gst_number'),
                    cinno=data1.get('cin_number')
                )
                messages.success(request, "Company info created successfully.")
            cmpy_info.save()
            info = cmpy_info  # Update `info` after saving or creating company info

        # Handle Address Form Submission
        elif 'address_type' in data1:  # Check for the address form
            address1 = UserAddress.objects.create(
                profile=data,
                company_name=data1.get('company-n'),  # Adjust based on your need
                address_type=data1.get('address_type'),
                street_address=data1.get('street_address'),
                city=data1.get('city'),
                state=data1.get('state')
            )
            address1.save()

        return redirect("accounts", id=id)

    address = UserAddress.objects.filter(profile=data)
    context = {'data': data, 'address': address, 'id': id, 'req': req, 'info': info}
    return render(request, "accounts.html", context)



@login_required
def invoice_view(request,id):
    # user = CustomUser.objects.get(id = id)
    # address = UserAddress.objects.get(profile = user)
    # order = Orders.objects.get(profile = user)
    # invoice = Invoice.objects.get(order = order)
    # print(invoice.invoice_id)
    # print(order)
    # print(user)
    # print(address)
    # context = {'address':address,'invoice':invoice,'user':user}
    return render(request,"invoice.html")


def dashboard_view(request):
    return render(request,'dashboard.html')

def TrackHome(request):
    return render(request,"Track1.html")

def TrackOrder(request):
    return render(request,"Track2.html")