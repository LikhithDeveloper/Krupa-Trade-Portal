from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.contrib.auth import get_user_model

# User = get_user_model()

# Custom user model
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=50,unique=True)
    password = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=10,unique=True,blank=True,null=True)
    gstin = models.CharField(max_length=20,unique=True,null=True)
    # phone_number = models.CharField(max_length=12)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # def __str__(self):
    #     return self.email

@receiver(post_save, sender=CustomUser)
def create_user_address(sender, instance, created, **kwargs):
    if created:  # This ensures the code runs only when a new user is created
        UserAddress.objects.create(
            profile=instance,
            address_type="Add your Address",
            street_address="Add your Address",
            city="Add your Address"
        )



# Category Model
class Category(models.Model):
    category_name = models.CharField(max_length=30)
    category_image = models.ImageField(null=True,blank=True)
    description = models.TextField()
    size = models.CharField(max_length=20,null=True,blank=True)
    date = models.DateField(null=True,blank=True)

    def __str__(self) -> str:
        return self.category_name

class Subcategory(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    sub_name = models.CharField(max_length=30)
    sub_image = models.ImageField(null=True,blank=True)
    description = models.TextField()
    size = models.CharField(max_length=20,null=True,blank=True)
    date = models.DateField(null=True,blank=True)

    def __str__(self) -> str:
        return self.sub_name

class Products(models.Model):
    product_image = models.ImageField(null=True,blank=True)
    product_name = models.CharField(max_length=50)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    brand = models.CharField(max_length=30,null=True,blank=True)
    size = models.CharField(max_length=20,null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    descripton = models.TextField()


    def __str__(self) -> str:
        return self.product_name

class Orders(models.Model):
    profile = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=10, unique=True, editable=False,blank=True)
    name = models.ForeignKey(Products, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    total = models.IntegerField()
    quantity = models.IntegerField()
    company = models.CharField(max_length=30)

    def save(self, *args, **kwargs):
        if not self.order_id:
            if last_order := Orders.objects.order_by('-id').first():
                self.order_id = str(int(last_order.order_id) + 1).zfill(5)
            else:
                self.order_id = '000001'  # Starting value
        super().save(*args, **kwargs)


from admin_panel.models import Managers

# from admin_panel.models import *
class Request(models.Model):
    profile = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=30)
    quantity = models.IntegerField()
    company = models.CharField(max_length=30)
    pincode = models.CharField(max_length=10)
    email = models.EmailField(max_length=30)
    mobile_number = models.CharField(max_length=10)
    price = models.IntegerField(blank=True,null=True)
    request = models.BooleanField(default=False, null=True,blank=True)
    type = models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True,blank=True,null=True)
    manager = models.ForeignKey(Managers,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return f'{self.company}-{self.id}'
    
@receiver(post_save, sender=Request)
def create_orders(sender, instance, created, **kwargs):
    if instance.request:
        from .models import Orders, Products
        try:
            product = Products.objects.get(product_name=instance.product_name)
            Orders.objects.create(
                profile=instance.profile,
                name=product,
                total=instance.price,
                quantity = instance.quantity,
                company = instance.company
            )
        except Products.DoesNotExist:
            print(f"Product with name {instance.product_name} does not exist.")



class CompanyInfo(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    company_name = models.CharField(max_length=30,null=True,blank=True)
    pan = models.CharField(max_length=30,null=True,blank=True)
    gstno = models.CharField(max_length=30,null=True,blank=True)
    cinno = models.CharField(max_length=30,null=True,blank=True)

class SupportTicket(models.Model):
    order_id = models.CharField(max_length=10, unique=True, editable=False, blank=True)
    profile = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    department = models.CharField(max_length=30)
    subject = models.CharField(max_length=50)
    message = models.TextField()
    additional_email = models.EmailField(max_length=50)
    answered = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)  # Make sure this is uncommented

    def save(self, *args, **kwargs):
        if not self.order_id:
            if last_order := SupportTicket.objects.order_by('-id').first():
                self.order_id = str(int(last_order.order_id) + 1).zfill(5)
            else:
                self.order_id = '000001'  # Starting value
        super().save(*args, **kwargs)


class UserAddress(models.Model):
    profile = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100,null=True,blank=True)
    address_type = models.TextField(null=True,blank=True)
    street_address = models.TextField(null=True,blank=True)
    city = models.TextField(null=True,blank=True)
    state = models.CharField(max_length=30,null=True,blank=True)



class Invoice(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    invoice_id = models.CharField(max_length=10,unique=True, editable=False,blank=True)
    date_created = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, null=True, blank=True)
    balance = models.IntegerField()
    paid = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.invoice_id:
            if last_invoice := Invoice.objects.order_by('-id').first():
                self.invoice_id = str(int(last_invoice.invoice_id) + 1).zfill(6)
            else:
                self.invoice_id = '000001'  # Starting value
        super().save(*args, **kwargs)





################ Estimate ##########################

class Estimate(models.Model):
    customer_name = models.ForeignKey(CustomUser, null=True, blank=True,on_delete=models.CASCADE)
    request = models.ForeignKey(Request, null=True, blank=True,on_delete=models.CASCADE)
    billing_address = models.TextField(null=True, blank=True)
    shipping_address = models.TextField(null=True, blank=True)
    place_of_supply = models.CharField(max_length=255, null=True, blank=True)
    estimate_number = models.CharField(max_length=100, null=True, blank=True)
    reference = models.CharField(max_length=100, null=True, blank=True)
    estimate_date = models.CharField(max_length=20,null=True, blank=True)
    expiry_date = models.CharField(max_length=20,null=True, blank=True)
    sales_person = models.CharField(max_length=255, null=True, blank=True)
    project_name = models.CharField(max_length=255, null=True, blank=True)
    subject = models.TextField(null=True, blank=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    shipping_charges = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    adjustment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    terms_and_conditions = models.TextField(null=True, blank=True)
    create_retainer_invoice = models.BooleanField(default=False)
    created_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=30,null=True,blank=True,default="SENT")

    def __str__(self):
        return f"New Estimates {self.estimate_number} - {self.request.company}"

class EstimateItem(models.Model):
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    item_details = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    discount = models.CharField(max_length=50, null=True, blank=True, default="0 %")
    tax = models.CharField(max_length=255, null=True, blank=True, default="Select a Tax")
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)

    def __str__(self):
        return f"Item {self.item_details} in Sales Order {self.estimate.estimate_number}"



################################# Sales Orders ######################################


class SalesOrder(models.Model):
    customer_name = models.ForeignKey(CustomUser, null=True, blank=True,on_delete=models.CASCADE)
    request = models.ForeignKey(Request, null=True, blank=True,on_delete=models.CASCADE)
    estimate = models.ForeignKey(Estimate,null=True,blank=True,on_delete=models.CASCADE)
    sales_order_number = models.CharField(max_length=100, blank=True)
    reference_number = models.CharField(max_length=100, blank=True)
    sales_order_date = models.CharField(max_length=100,null=True, blank=True)
    expected_shipment_date = models.CharField(max_length=100,null=True, blank=True)
    payment_terms = models.CharField(max_length=255, blank=True)
    delivery_method = models.CharField(max_length=255, blank=True)
    sales_person = models.CharField(max_length=255, blank=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    terms_and_conditions = models.TextField(blank=True)
    create_retainer_invoice = models.BooleanField(default=False)
    created_date = models.DateField(auto_now=True)
    satus = models.CharField(max_length=30,null=True,blank=True,default="SENT")

    def __str__(self):
        return f"Sales Order {self.sales_order_number} - {self.request.company}"


class SalesOrderItem(models.Model):
    sales_order = models.ForeignKey(SalesOrder, related_name='items', on_delete=models.CASCADE)
    item_details = models.CharField(max_length=255, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.CharField(max_length=50, blank=True, default="0 %")
    tax = models.CharField(max_length=100, blank=True, default="Select a Tax")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Item {self.item_details} in Sales Order {self.sales_order.sales_order_number}"




################################# Invoices ######################################

class InvoiceEstimate(models.Model):
    customer_name = models.ForeignKey(CustomUser, null=True, blank=True,on_delete=models.CASCADE)
    request = models.ForeignKey(Request, null=True, blank=True,on_delete=models.CASCADE)
    estimate = models.ForeignKey(Estimate,null=True,blank=True,on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100, blank=True)
    order_number = models.CharField(max_length=100, blank=True)
    invoice_date = models.CharField(max_length=30,null=True, blank=True)
    terms = models.TextField(blank=True)
    due_date = models.CharField(max_length=30,null=True, blank=True)
    sales_person = models.CharField(max_length=255, blank=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    terms_and_conditions = models.TextField(blank=True)
    create_retainer_invoice = models.BooleanField(default=False)
    created_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=30,null=True,blank=True, default="PENDING")

    def __str__(self):
        return f"Invoice {self.invoice_number} for {self.request.company}"
    


class Item(models.Model):
    invoice = models.ForeignKey(InvoiceEstimate, on_delete=models.CASCADE, related_name='items')
    item_details = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.CharField(max_length=10, default="0 %")
    tax = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.item_details



#################################### Payments #######################################

class Payment(models.Model):
    customer_name = models.ForeignKey(CustomUser, null=True, blank=True,on_delete=models.CASCADE)
    request = models.ForeignKey(Request, null=True, blank=True,on_delete=models.CASCADE)
    amount_received = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    bank_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    payment_date = models.CharField(max_length = 30,null=True, blank=True)
    payment_number = models.CharField(max_length=50, null=True, blank=True)
    payment_mode = models.CharField(max_length=50, null=True, blank=True)
    deposited_to = models.CharField(max_length=255, null=True, blank=True)
    reference = models.CharField(max_length=255, null=True, blank=True)
    tax_deducted = models.CharField(max_length=3, default='yes', null=True, blank=True)
    reference_number = models.CharField(max_length=50, null=True, blank=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    shipping_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    created_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"Payment by {self.customer_name} - {self.total}"
    




##############################  VENDORS MODELS   ################################


from django.db import models

class Vendor(models.Model):
    salutation = models.CharField(max_length=50, null=True, blank=True)
    firstname = models.CharField(max_length=100, null=True, blank=True)
    lastname = models.CharField(max_length=100, null=True, blank=True)
    companyname = models.CharField(max_length=200, null=True, blank=True)
    vendoremail = models.EmailField(null=True, blank=True)
    vendorphone1 = models.CharField(max_length=15, null=True, blank=True)
    vendorphone2 = models.CharField(max_length=15, null=True, blank=True)
    gst_Treatment = models.CharField(max_length=50, null=True, blank=True)
    sourceofsupply = models.CharField(max_length=100, null=True, blank=True)
    pan = models.CharField(max_length=20, null=True, blank=True)
    currency = models.CharField(max_length=10, null=True, blank=True)
    openingbalance = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    paymentterms = models.CharField(max_length=100, null=True, blank=True)
    pricelist = models.CharField(max_length=100, null=True, blank=True)
    enableportal = models.BooleanField(default=False, null=True, blank=True)
    portallanguage = models.CharField(max_length=50, null=True, blank=True)
    documents = models.TextField(null=True, blank=True)
    billingattention = models.CharField(max_length=200, null=True, blank=True)
    billingcountry = models.CharField(max_length=100, null=True, blank=True)
    billingaddress1 = models.TextField(null=True, blank=True)
    billingaddress2 = models.TextField(null=True, blank=True)
    billingcity = models.CharField(max_length=100, null=True, blank=True)
    billingstate = models.CharField(max_length=100, null=True, blank=True)
    billingpincode = models.CharField(max_length=10, null=True, blank=True)
    billingphone = models.CharField(max_length=15, null=True, blank=True)
    shippingattention = models.CharField(max_length=200, null=True, blank=True)
    shippingcountry = models.CharField(max_length=100, null=True, blank=True)
    shippingaddress1 = models.TextField(null=True, blank=True)
    shippingaddress2 = models.TextField(null=True, blank=True)
    shippingcity = models.CharField(max_length=100, null=True, blank=True)
    shippingstate = models.CharField(max_length=100, null=True, blank=True)
    shippingpincode = models.CharField(max_length=10, null=True, blank=True)
    shippingphone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.companyname}"




class Purchase(models.Model):
    vendor_name = models.CharField(max_length=255, blank=True, null=True)
    source_of_supply = models.CharField(max_length=255, blank=True, null=True)
    destination_of_supply = models.CharField(max_length=255, blank=True, null=True)
    purchase_order = models.CharField(max_length=255, blank=True, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=30, blank=True, null=True)
    expected_delivery_date = models.CharField(max_length=30, blank=True, null=True)
    payment_terms = models.CharField(max_length=255, blank=True, null=True)
    item_tax = models.CharField(max_length=50, blank=True, null=True)
    price_list = models.CharField(max_length=50, blank=True, null=True)
    discount = models.CharField(max_length=50, blank=True, null=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    shipping_charges = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    adjustment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    created_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=30,null=True,blank=True, default="OPEN")

class PurchaseItem(models.Model):
    invoice = models.ForeignKey(Purchase, related_name='items', on_delete=models.CASCADE)
    item_details = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=0.00)
    tax = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)


from django.db import models

class Bill(models.Model):
    vendor_name = models.CharField(max_length=255, blank=True, null=True)
    source_of_supply = models.CharField(max_length=255, blank=True, null=True)
    destination_of_supply = models.CharField(max_length=255, blank=True, null=True)
    bill_number = models.CharField(max_length=255, blank=True, null=True)  # ordernumber
    reference = models.CharField(max_length=255, blank=True, null=True)  # bill reference
    bill_date = models.CharField(max_length=30,blank=True, null=True)  # billdate
    due_date = models.CharField(max_length=30,blank=True, null=True)  # duedate
    payment_terms = models.CharField(max_length=255, blank=True, null=True)
    item_tax = models.CharField(max_length=50, blank=True, null=True, default="none")
    price_list = models.CharField(max_length=50, blank=True, null=True, default="none")
    discount = models.CharField(max_length=50, blank=True, null=True, default="none")
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    shipping_charges = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    adjustment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    created_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=30, null=True, blank=True, default="OPEN")

class BillItem(models.Model):
    bill = models.ForeignKey(Bill, related_name='items', on_delete=models.CASCADE)
    item_details = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=0.00)
    tax = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
