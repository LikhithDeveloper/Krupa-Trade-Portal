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
            # Generate a unique sequential order ID
            last_order = Orders.objects.order_by('-id').first()
            if last_order:
                last_id = int(last_order.order_id)
                self.order_id = str(last_id + 1).zfill(5)  # Increment and pad with zeros
            else:
                self.order_id = '000001'  # Starting value
        super().save(*args, **kwargs)


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
            # Generate a unique sequential order ID
            last_order = SupportTicket.objects.order_by('-id').first()
            if last_order:
                last_id = int(last_order.order_id)
                self.order_id = str(last_id + 1).zfill(5)  # Increment and pad with zeros
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
            # Generate a unique sequential invoice ID
            last_invoice = Invoice.objects.order_by('-id').first()     
            if last_invoice:
                last_id = int(last_invoice.invoice_id)
                self.invoice_id = str(last_id + 1).zfill(6)  # Increment and pad with zeros
            else:
                self.invoice_id = '000001'  # Starting value
        super().save(*args, **kwargs)


