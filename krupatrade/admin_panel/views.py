from django.shortcuts import render,HttpResponse
from krupa.models import *
from admin_panel.models import Managers
from django.core import serializers
from django.core.serializers import serialize
from rest_framework.renderers import JSONRenderer
from .serializer import *

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

def Customers(request):  # sourcery skip: avoid-builtin-shadow
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

def Estimates(request):
    return render(request,"Estimates.html")

def Estimates2(request):
    return render(request,"Estimates2.html")

def Newestimates(request):
    if request.method == "POST":
        print(request.POST)
    return render(request,"newestimates.html")