from django.contrib import admin
from django.urls import path
from admin_panel.views import AdminProducts,AddProducts,AddSubCategories,AddCategories,Leads1,Leads2,Leads3,Customers,ManagersView,AddManagers,Estimates,Estimates2,Newestimates,Invoice1,Invoice2,Invoice3,Newsalesorder,SalesOrder1,Payment1,Newpayment,Payment2,Coverter_Invoice,SalesOrder2, Coverter_Invoice_sales,Create_invoice_sales,InvoiceReal,PaymentInvoice
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('adminproducts/',AdminProducts,name="AdminProducts"),
    path('addproducts/',AddProducts,name="AddProducts"),
    path('addsubcategories/',AddSubCategories,name="AddSubCategories"),
    path('addcategories/',AddCategories,name="AddCategories"),
    path('leadsall/',Leads1,name='Leads1'),
    path('leadsbuyer/',Leads2,name='Leads2'),
    path('leadsseller/',Leads3,name='Leads3'),
    path('customerspage/',Customers,name='Customers'),
    path('managers/',ManagersView,name="ManagersView"),
    path('addmanagers/',AddManagers,name="AddManagers"),
    path('estimates/',Estimates,name="Estimates"),
    path('estimates2/<int:id>/',Estimates2,name="Estimate2"),
    path('createinvoice/<int:id>/',Coverter_Invoice,name="Coverter_Invoice"),
    path('newestimates/',Newestimates,name='Newestimates'),
    path('invoice1/',Invoice1,name="Invoice1"),
    path('invoice2/<int:id>/',Invoice2,name="Invoice2"),
    path('realinvoice/',InvoiceReal,name="InvoiceReal"),
    path('newinvoice/',Invoice3,name="Invoice3"),
    path('salesorder1/',SalesOrder1,name="SalesOrder1"),
    path('salesorder2/<int:id>/',SalesOrder2,name="SalesOrder2"),
    path('createinvoicesale/<int:id>/',Coverter_Invoice_sales,name="Coverter_Invoice_sales"),
    path('salesinvoice/',Create_invoice_sales,name="Create_invoice_sales"),
    path('newsalesorder/',Newsalesorder,name="Newsalesorder"),
    path('payment1/',Payment1,name="Payment1"),
    path('payment2/<int:id>/',Payment2,name="Payment2"),
    path('paymentinvoice/',PaymentInvoice,name="PaymentInvoice"),
    path('newpayment/',Newpayment,name="Newpayment"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)