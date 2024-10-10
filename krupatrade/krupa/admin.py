from django.contrib import admin
from .models import CustomUser, Category, Products, Subcategory, Orders, Request, SupportTicket, UserAddress, Invoice
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Products)
admin.site.register(Orders)
admin.site.register(Request)
admin.site.register(SupportTicket)
admin.site.register(UserAddress)
admin.site.register(Invoice)


