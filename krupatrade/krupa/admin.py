from django.contrib import admin
# from .models import CustomUser, Category, Products, Subcategory, Orders, Request, SupportTicket, UserAddress, Invoice, Estimate, EstimateItem
from .models import*
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
admin.site.register(EstimateItem)
admin.site.register(Estimate)
admin.site.register(InvoiceEstimate)
admin.site.register(Item)


