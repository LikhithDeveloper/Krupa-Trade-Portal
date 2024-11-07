from django.contrib import admin
from django.urls import path
# from admin_panel.views import AdminProducts,AddProducts,AddSubCategories,AddCategories,Leads1,Leads2,Leads3,Customers,ManagersView,AddManagers,Estimates,Estimates2,Newestimates,Invoice1,Invoice2,Invoice3,Newsalesorder,SalesOrder1,Payment1,Newpayment,Payment2,Coverter_Invoice,SalesOrder2, Coverter_Invoice_sales,Create_invoice_sales,InvoiceReal,PaymentInvoice,Create_invoice_estimates,Coverter_Sales
from django.conf import settings
from django.conf.urls.static import static
from admin_panel.views import*

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
    path('estimatetosales/<int:id>/',Coverter_Sales,name="Coverter_Sales"),
    path('estimateinvoice/<int:id>/',Create_invoice_estimates,name="Create_invoice_estimates"),
    path('newestimates/',Newestimates,name='Newestimates'),
    path('invoice1/',Invoice1,name="Invoice1"),
    path('invoice2/<int:id>/',Invoice2,name="Invoice2"),
    path('realinvoice/<int:id>/',InvoiceReal,name="InvoiceReal"),
    path('newinvoice/',Invoice3,name="Invoice3"),
    path('salesorder1/',SalesOrder1,name="SalesOrder1"),
    path('salesorder2/<int:id>/',SalesOrder2,name="SalesOrder2"),
    path('createinvoicesale/<int:id>/',Coverter_Invoice_sales,name="Coverter_Invoice_sales"),
    path('salesinvoice/<int:id>/',Create_invoice_sales,name="Create_invoice_sales"),
    path('newsalesorder/',Newsalesorder,name="Newsalesorder"),
    path('payment1/',Payment1,name="Payment1"),
    path('payment2/<int:id>/',Payment2,name="Payment2"),
    path('paymentinvoice/',PaymentInvoice,name="PaymentInvoice"),
    path('newpayment/',Newpayment,name="Newpayment"),

    ############### VENDORS urls #################
    path('vendors1/',Vendors1,name="Vendors1"),
    path('vendors2/<int:id>/',Vendors2,name="Vendors2"),
    path('vendors3/',Vendors3,name="Vendors3"),


    path('purchases1/',Purchases1,name="Purchases1"),
    path('purchases2/<int:id>/',Purchases2,name="Purchases2"),
    path('purchasestobill/<int:id>/',PurchasesToBill,name = "PurchasesToBill"),
    path('purchases3/',Purchases3,name="Purchases3"),

    path('bills1/',Bills1,name="Bills1"),
    path('bills2/<int:id>/',Bills2,name="Bills2"),
    path('bills3/',Bills3,name="Bills3"),

    path('paymentsvendor1/',Payment1,name="Payment1"),
    path('paymentsvendor2/',Payment2,name="Payment2"),
    path('paymentsvendor3/',Payment3,name="Payment3"),

    path('expanses1/',Expansens1,name="Expansens1"),
    path('expanses2/',Expansens2,name="Expansens2"),
    path('expanses3/',Expansens3,name="Expansens3"),

    path('recurring1/',ReccuringExpanses1,name="ReccuringExpanses1"),
    path('recurring2/',ReccuringExpanses2,name="ReccuringExpanses2"),
    path('recurring3/',ReccuringExpanses3,name="ReccuringExpanses3"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)